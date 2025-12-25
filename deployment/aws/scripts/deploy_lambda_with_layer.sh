#!/bin/bash
set -e

# Disable AWS CLI pager
export AWS_PAGER=""

echo "🚀 Deploying to AWS Lambda with Custom Layer"
echo "=============================================="

FUNCTION_NAME="wine-quality-predictor"
BUCKET_NAME="wine-quality-mlops-sujan"
REGION="us-east-2"
RUNTIME="python3.12"
LAYER_NAME="sklearn-numpy-scipy-layer"

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ Error: AWS credentials not configured"
    echo "💡 Run: aws configure"
    exit 1
fi

echo "✅ AWS credentials verified"
echo ""

# Step 1: Build and publish Lambda Layer (if not exists)
echo "🏗️  Step 1: Creating Lambda Layer..."
LAYER_ARN=$(aws lambda list-layer-versions --layer-name "$LAYER_NAME" --region "$REGION" --query 'LayerVersions[0].LayerVersionArn' --output text 2>/dev/null || echo "")

if [ -z "$LAYER_ARN" ] || [ "$LAYER_ARN" == "None" ]; then
    echo "📦 Building new Lambda Layer..."

    # Create layer directory structure
    mkdir -p lambda_layer/python
    cd lambda_layer/python

    # Install dependencies for the layer
    echo "📦 Installing scikit-learn, numpy, scipy, joblib..."
    pip install \
        scikit-learn \
        numpy \
        scipy \
        joblib \
        --target . \
        --platform manylinux2014_x86_64 \
        --implementation cp \
        --python-version 3.12 \
        --only-binary=:all: \
        --upgrade \
        -q

    echo "🧹 Cleaning up layer..."
    # Aggressive cleanup - but keep numpy.f2py (needed by sklearn)
    find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*.pyx" -delete
    find . -name "*.c" -delete
    find . -name "*.h" -delete
    find . -name "*.md" -delete
    rm -rf ./sklearn/datasets 2>/dev/null || true
    rm -rf ./numpy/tests 2>/dev/null || true
    # Keep numpy/f2py - it's needed by numpy imports
    rm -rf ./scipy/tests 2>/dev/null || true
    rm -rf ./scipy/integrate 2>/dev/null || true
    rm -rf ./scipy/interpolate 2>/dev/null || true
    rm -rf ./scipy/signal 2>/dev/null || true
    rm -rf ./scipy/stats 2>/dev/null || true
    rm -rf ./scipy/ndimage 2>/dev/null || true
    rm -rf ./scipy/spatial 2>/dev/null || true
    rm -rf ./scipy/special 2>/dev/null || true

    cd ..

    # Create zip for layer
    echo "🗜️  Creating layer zip..."
    zip -r ../sklearn_layer.zip python -q

    cd ..
    rm -rf lambda_layer

    # Upload layer to S3
    LAYER_S3_KEY="lambda-layers/sklearn_layer_$(date +%Y%m%d_%H%M%S).zip"
    echo "📤 Uploading layer to S3..."
    aws s3 cp sklearn_layer.zip "s3://${BUCKET_NAME}/${LAYER_S3_KEY}" --region "$REGION"

    # Publish Lambda Layer from S3
    echo "🚀 Publishing Lambda Layer..."
    LAYER_ARN=$(aws lambda publish-layer-version \
        --layer-name "$LAYER_NAME" \
        --description "Scikit-learn, NumPy, SciPy, Joblib for Python 3.12" \
        --content "S3Bucket=${BUCKET_NAME},S3Key=${LAYER_S3_KEY}" \
        --compatible-runtimes python3.12 \
        --region "$REGION" \
        --query 'LayerVersionArn' \
        --output text)

    rm -f sklearn_layer.zip
    echo "✅ Layer published: $LAYER_ARN"
else
    echo "✅ Using existing layer: $LAYER_ARN"
fi

echo ""

# Step 2: Create minimal deployment package (handler only)
echo "📦 Step 2: Creating minimal deployment package..."
mkdir -p lambda_package
cd lambda_package

# Copy Lambda handler (from deployment/aws/lambda/)
cp "$(dirname "$0")/../lambda/handler.py" lambda_handler.py

# Copy s3_utils (from src/utils/)
mkdir -p src/utils
cp "$(dirname "$0")/../../../src/utils/s3_utils.py" src/utils/ 2>/dev/null || true
touch src/__init__.py
touch src/utils/__init__.py

# NO dependencies installed - they come from layer
echo "📏 Package size: $(du -sh . | cut -f1)"

# Create zip file
echo "🗜️  Creating deployment zip..."
zip -r ../lambda_deployment.zip . -q

cd ..
rm -rf lambda_package

echo "✅ Minimal deployment package created"
echo ""

# Upload deployment package to S3
S3_PACKAGE_KEY="lambda-deployments/lambda_deployment_$(date +%Y%m%d_%H%M%S).zip"

echo "📤 Step 3: Uploading deployment package to S3..."
aws s3 cp lambda_deployment.zip "s3://${BUCKET_NAME}/${S3_PACKAGE_KEY}" \
    --region "$REGION"
echo "✅ Package uploaded"
echo ""

# Create IAM role for Lambda
echo "🔐 Step 4: Ensuring IAM role exists..."
ROLE_NAME="wine-quality-lambda-role"

if aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "✅ IAM role already exists"
else
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

    aws iam attach-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

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
    echo "✅ IAM role created"
    sleep 10
fi

ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)
echo ""

# Deploy or update Lambda function
echo "🔧 Step 5: Deploying Lambda function with Layer..."
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" &>/dev/null; then
    echo "🔄 Updating existing function..."

    # Update code
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --s3-bucket "$BUCKET_NAME" \
        --s3-key "$S3_PACKAGE_KEY" \
        --region "$REGION"

    # Wait for update
    echo "⏳ Waiting for code update..."
    aws lambda wait function-updated --function-name "$FUNCTION_NAME" --region "$REGION"

    # Update configuration with layer
    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --timeout 30 \
        --memory-size 1024 \
        --layers "$LAYER_ARN" \
        --environment "Variables={S3_BUCKET_NAME=${BUCKET_NAME}}" \
        --region "$REGION"
else
    echo "✨ Creating new function..."
    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --role "$ROLE_ARN" \
        --handler lambda_handler.lambda_handler \
        --code "S3Bucket=${BUCKET_NAME},S3Key=${S3_PACKAGE_KEY}" \
        --layers "$LAYER_ARN" \
        --timeout 30 \
        --memory-size 1024 \
        --environment "Variables={S3_BUCKET_NAME=${BUCKET_NAME}}" \
        --region "$REGION"
fi

echo "✅ Lambda function deployed"
echo ""

# Create API Gateway
echo "🌐 Step 6: Setting up API Gateway..."

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

    aws lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id apigateway-invoke \
        --action lambda:InvokeFunction \
        --principal apigateway.amazonaws.com \
        --source-arn "arn:aws:execute-api:${REGION}:$(aws sts get-caller-identity --query Account --output text):${API_ID}/*/*" \
        --region "$REGION" || true

    echo "✅ API Gateway created"
else
    echo "✅ API Gateway already exists"
fi

API_ENDPOINT=$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?ApiId=='${API_ID}'].ApiEndpoint" --output text)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔗 API Endpoint:"
echo "   ${API_ENDPOINT}"
echo ""
echo "📦 Lambda Layer: $LAYER_ARN"
echo "📦 Package: s3://${BUCKET_NAME}/${S3_PACKAGE_KEY}"
echo ""
echo "📝 Test with curl:"
echo "   curl -X POST ${API_ENDPOINT} \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"fixed_acidity\":7.4,\"volatile_acidity\":0.7,\"citric_acid\":0,\"residual_sugar\":1.9,\"chlorides\":0.076,\"free_sulfur_dioxide\":11,\"total_sulfur_dioxide\":34,\"density\":0.9978,\"pH\":3.51,\"sulphates\":0.56,\"alcohol\":9.4,\"wine_type_encoded\":0}'"

# Cleanup
rm -f lambda_deployment.zip
echo ""
echo "✅ Cleanup complete!"
