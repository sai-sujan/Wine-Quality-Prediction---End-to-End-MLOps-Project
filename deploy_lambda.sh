#!/bin/bash
set -e

# Disable AWS CLI pager
export AWS_PAGER=""

echo "🚀 Deploying to AWS Lambda"
echo "==========================="

FUNCTION_NAME="wine-quality-predictor"
BUCKET_NAME="wine-quality-mlops-sujan"
REGION="us-east-2"
RUNTIME="python3.12"

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ Error: AWS credentials not configured"
    echo "💡 Run: aws configure"
    exit 1
fi

echo "✅ AWS credentials verified"
echo ""

# Create deployment package directory
echo "📦 Creating deployment package..."
mkdir -p lambda_package
cd lambda_package

# Copy Lambda handler
cp ../lambda_handler.py .

# Copy only s3_utils.py (not entire src folder)
mkdir -p src
cp ../src/s3_utils.py src/ 2>/dev/null || touch src/__init__.py

# Install scikit-learn with minimal dependencies
echo "📦 Installing scikit-learn + essential dependencies..."
pip install --target . \
    scikit-learn \
    pandas \
    numpy \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    --upgrade \
    -q

# Remove ALL unnecessary files to stay under 250MB (Lambda unzipped limit)
echo "🧹 Aggressive cleanup..."
find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyx" -delete
find . -name "*.c" -delete
find . -name "*.h" -delete
rm -rf ./sklearn/datasets 2>/dev/null || true
rm -rf ./pandas/tests 2>/dev/null || true
rm -rf ./numpy/tests 2>/dev/null || true
rm -rf ./scipy/tests 2>/dev/null || true
rm -rf ./joblib/test 2>/dev/null || true
rm -rf ./*.dist-info 2>/dev/null || true

# Check package size
PACKAGE_SIZE=$(du -sh . | cut -f1)
echo "📏 Package size: $PACKAGE_SIZE"

# Create zip file (exclude unnecessary files)
echo "🗜️  Creating deployment zip..."
zip -r ../lambda_deployment.zip . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "*.dist-info/*" \
    -q

cd ..
rm -rf lambda_package

echo "✅ Deployment package created: lambda_deployment.zip"
echo ""

# Create IAM role for Lambda
echo "🔐 Creating IAM role..."
ROLE_NAME="wine-quality-lambda-role"

# Check if role exists
if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "✅ IAM role already exists: $ROLE_NAME"
else
    # Create trust policy
    cat > /tmp/trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

    aws iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document file:///tmp/trust-policy.json \
        --region "$REGION"

    # Attach policies
    aws iam attach-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    # Create S3 access policy
    cat > /tmp/s3-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${BUCKET_NAME}/*",
        "arn:aws:s3:::${BUCKET_NAME}"
      ]
    }
  ]
}
EOF

    aws iam put-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-name "S3AccessPolicy" \
        --policy-document file:///tmp/s3-policy.json

    rm /tmp/trust-policy.json /tmp/s3-policy.json

    echo "✅ IAM role created: $ROLE_NAME"
    echo "⏳ Waiting 10s for IAM role to propagate..."
    sleep 10
fi

# Get role ARN
ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

# Create or update Lambda function
echo "🔧 Deploying Lambda function..."
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" &>/dev/null; then
    echo "🔄 Updating existing function..."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file fileb://lambda_deployment.zip \
        --region "$REGION"

    # Wait for update to complete before updating configuration
    echo "⏳ Waiting for code update..."
    aws lambda wait function-updated --function-name "$FUNCTION_NAME" --region "$REGION"

    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --timeout 30 \
        --memory-size 1024 \
        --environment "Variables={S3_BUCKET_NAME=${BUCKET_NAME}}" \
        --region "$REGION"
else
    echo "✨ Creating new function..."
    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --role "$ROLE_ARN" \
        --handler lambda_handler.lambda_handler \
        --zip-file fileb://lambda_deployment.zip \
        --timeout 30 \
        --memory-size 1024 \
        --environment "Variables={S3_BUCKET_NAME=${BUCKET_NAME}}" \
        --region "$REGION"
fi

echo "✅ Lambda function deployed: $FUNCTION_NAME"
echo ""

# Create API Gateway
echo "🌐 Setting up API Gateway..."

# Check if API exists
API_ID=$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?Name=='${FUNCTION_NAME}-api'].ApiId" --output text)

if [ -z "$API_ID" ]; then
    echo "✨ Creating new API Gateway..."
    API_ID=$(aws apigatewayv2 create-api \
        --name "${FUNCTION_NAME}-api" \
        --protocol-type HTTP \
        --target "arn:aws:lambda:${REGION}:$(aws sts get-caller-identity --query Account --output text):function:${FUNCTION_NAME}" \
        --region "$REGION" \
        --query 'ApiId' \
        --output text)

    # Add Lambda permission for API Gateway
    aws lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id apigateway-invoke \
        --action lambda:InvokeFunction \
        --principal apigateway.amazonaws.com \
        --source-arn "arn:aws:execute-api:${REGION}:$(aws sts get-caller-identity --query Account --output text):${API_ID}/*/*" \
        --region "$REGION" || true

    echo "✅ API Gateway created"
else
    echo "✅ API Gateway already exists: $API_ID"
fi

# Get API endpoint
API_ENDPOINT=$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?ApiId=='${API_ID}'].ApiEndpoint" --output text)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 API Endpoint:"
echo "   ${API_ENDPOINT}"
echo ""
echo "📝 Test with curl:"
echo "   curl -X POST ${API_ENDPOINT} \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"fixed_acidity\":7.4,\"volatile_acidity\":0.7,\"citric_acid\":0,\"residual_sugar\":1.9,\"chlorides\":0.076,\"free_sulfur_dioxide\":11,\"total_sulfur_dioxide\":34,\"density\":0.9978,\"pH\":3.51,\"sulphates\":0.56,\"alcohol\":9.4,\"wine_type_encoded\":0}'"
echo ""
echo "🎨 Update Streamlit Dashboard:"
echo "   Set AWS Lambda URL to: ${API_ENDPOINT}"
echo ""
echo "📊 View Lambda logs:"
echo "   aws logs tail /aws/lambda/${FUNCTION_NAME} --follow --region ${REGION}"
