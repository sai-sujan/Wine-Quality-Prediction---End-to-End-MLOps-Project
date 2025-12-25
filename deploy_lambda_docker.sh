#!/bin/bash
set -e

# Disable AWS CLI pager
export AWS_PAGER=""

echo "🐳 Deploying Lambda with Docker Container"
echo "=========================================="

FUNCTION_NAME="wine-quality-predictor"
REGION="us-east-2"
BUCKET_NAME="wine-quality-mlops-sujan"

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_NAME="wine-quality-lambda"
IMAGE_TAG="latest"

echo "📋 Configuration:"
echo "  Account ID: $ACCOUNT_ID"
echo "  Region: $REGION"
echo "  ECR Repo: $ECR_REPO_NAME"
echo ""

# Step 1: Create ECR repository if it doesn't exist
echo "🏗️  Step 1: Setting up ECR repository..."
if ! aws ecr describe-repositories --repository-names "$ECR_REPO_NAME" --region "$REGION" &>/dev/null; then
    echo "Creating ECR repository..."
    aws ecr create-repository \
        --repository-name "$ECR_REPO_NAME" \
        --region "$REGION"
    echo "✅ ECR repository created"
else
    echo "✅ ECR repository already exists"
fi

ECR_URI="${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME}"
echo ""

# Step 2: Build Docker image
echo "🐳 Step 2: Building Docker image..."
docker build --platform linux/amd64 -t "$ECR_REPO_NAME:$IMAGE_TAG" .
echo "✅ Docker image built"
echo ""

# Step 3: Login to ECR
echo "🔐 Step 3: Logging in to ECR..."
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$ECR_URI"
echo "✅ Logged in to ECR"
echo ""

# Step 4: Tag and push image
echo "📤 Step 4: Pushing image to ECR..."
docker tag "$ECR_REPO_NAME:$IMAGE_TAG" "$ECR_URI:$IMAGE_TAG"
docker push "$ECR_URI:$IMAGE_TAG"
echo "✅ Image pushed to ECR"
echo ""

# Step 5: Create or update Lambda function
echo "🔧 Step 5: Deploying Lambda function..."

# Check if IAM role exists
ROLE_NAME="wine-quality-lambda-role"
if ! aws iam get-role --role-name "$ROLE_NAME" &>/dev/null; then
    echo "Creating IAM role..."
    
    cat > /tmp/trust-policy.json <<POLICY
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
POLICY

    aws iam create-role \
        --role-name "$ROLE_NAME" \
        --assume-role-policy-document file:///tmp/trust-policy.json

    aws iam attach-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    cat > /tmp/s3-policy.json <<POLICY
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
POLICY

    aws iam put-role-policy \
        --role-name "$ROLE_NAME" \
        --policy-name "S3AccessPolicy" \
        --policy-document file:///tmp/s3-policy.json

    rm /tmp/trust-policy.json /tmp/s3-policy.json
    echo "⏳ Waiting for IAM role to propagate..."
    sleep 10
fi

ROLE_ARN=$(aws iam get-role --role-name "$ROLE_NAME" --query 'Role.Arn' --output text)

# Create or update Lambda function
if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" &>/dev/null; then
    echo "🔄 Updating existing function..."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --image-uri "$ECR_URI:$IMAGE_TAG" \
        --region "$REGION"
    
    echo "⏳ Waiting for update..."
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
        --package-type Image \
        --code ImageUri="$ECR_URI:$IMAGE_TAG" \
        --role "$ROLE_ARN" \
        --timeout 30 \
        --memory-size 1024 \
        --environment "Variables={S3_BUCKET_NAME=${BUCKET_NAME}}" \
        --region "$REGION"
fi

echo "✅ Lambda function deployed"
echo ""

# Step 6: Setup API Gateway
echo "🌐 Step 6: Setting up API Gateway..."
API_ID=$(aws apigatewayv2 get-apis --region "$REGION" --query "Items[?Name=='${FUNCTION_NAME}-api'].ApiId" --output text)

if [ -z "$API_ID" ]; then
    echo "✨ Creating new API Gateway..."
    API_ID=$(aws apigatewayv2 create-api \
        --name "${FUNCTION_NAME}-api" \
        --protocol-type HTTP \
        --target "arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${FUNCTION_NAME}" \
        --region "$REGION" \
        --query 'ApiId' \
        --output text)

    aws lambda add-permission \
        --function-name "$FUNCTION_NAME" \
        --statement-id apigateway-invoke \
        --action lambda:InvokeFunction \
        --principal apigateway.amazonaws.com \
        --source-arn "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:${API_ID}/*/*" \
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
echo "🐳 Docker Image: $ECR_URI:$IMAGE_TAG"
echo ""
echo "📝 Test with curl:"
echo "   curl -X POST ${API_ENDPOINT} \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"fixed_acidity\":7.4,\"volatile_acidity\":0.7,\"citric_acid\":0,\"residual_sugar\":1.9,\"chlorides\":0.076,\"free_sulfur_dioxide\":11,\"total_sulfur_dioxide\":34,\"density\":0.9978,\"pH\":3.51,\"sulphates\":0.56,\"alcohol\":9.4,\"wine_type_encoded\":0}'"
echo ""
