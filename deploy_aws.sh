#!/bin/bash
set -e

echo "🚀 Deploying Customer Satisfaction Prediction API to AWS Lambda"
echo "================================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed${NC}"
    echo "Install it from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo -e "${RED}❌ AWS SAM CLI is not installed${NC}"
    echo "Install it from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html"
    echo ""
    echo "Quick install on macOS:"
    echo "  brew install aws-sam-cli"
    exit 1
fi

# Check AWS credentials
echo -e "${YELLOW}📋 Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured${NC}"
    echo "Run: aws configure"
    exit 1
fi

echo -e "${GREEN}✓ AWS credentials configured${NC}"

# Get AWS account ID and region
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")

echo -e "${YELLOW}📍 Using AWS Account: ${AWS_ACCOUNT_ID}${NC}"
echo -e "${YELLOW}📍 Using AWS Region: ${AWS_REGION}${NC}"

# Stack name
STACK_NAME="customer-satisfaction-mlops"

# Build the Lambda function
echo -e "\n${YELLOW}🔨 Building Lambda function...${NC}"
sam build --template-file template.yaml

# Package the application
echo -e "\n${YELLOW}📦 Packaging application...${NC}"
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket "${STACK_NAME}-deployment-${AWS_ACCOUNT_ID}" \
    --region ${AWS_REGION} \
    || {
        echo -e "${YELLOW}Creating deployment bucket...${NC}"
        aws s3 mb "s3://${STACK_NAME}-deployment-${AWS_ACCOUNT_ID}" --region ${AWS_REGION}
        sam package \
            --output-template-file packaged.yaml \
            --s3-bucket "${STACK_NAME}-deployment-${AWS_ACCOUNT_ID}" \
            --region ${AWS_REGION}
    }

# Deploy the application
echo -e "\n${YELLOW}🚀 Deploying to AWS...${NC}"
sam deploy \
    --template-file packaged.yaml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_IAM \
    --region ${AWS_REGION} \
    --no-confirm-changeset \
    --no-fail-on-empty-changeset

# Get outputs
echo -e "\n${GREEN}✅ Deployment complete!${NC}"
echo -e "\n${YELLOW}📊 Stack Outputs:${NC}"
aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
    --output table

# Get API URL
API_URL=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`PredictionEndpoint`].OutputValue' \
    --output text)

MODEL_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`ModelBucketName`].OutputValue' \
    --output text)

echo -e "\n${GREEN}🎉 Deployment Successful!${NC}"
echo -e "\n${YELLOW}📝 Next Steps:${NC}"
echo "1. Upload your trained model to S3:"
echo -e "   ${GREEN}./upload_model.sh${NC}"
echo ""
echo "2. Test the API:"
echo -e "   ${GREEN}curl -X POST ${API_URL} \\
     -H 'Content-Type: application/json' \\
     -d '{
       \"payment_sequential\": 1,
       \"payment_installments\": 3,
       \"payment_value\": 100.0,
       \"price\": 80.0,
       \"freight_value\": 10.0,
       \"product_name_lenght\": 50,
       \"product_description_lenght\": 200,
       \"product_photos_qty\": 3,
       \"product_weight_g\": 1000,
       \"product_length_cm\": 20,
       \"product_height_cm\": 10,
       \"product_width_cm\": 15
     }'${NC}"
echo ""
echo "3. Share your API endpoint:"
echo -e "   ${GREEN}${API_URL}${NC}"
echo ""
echo "4. Model bucket:"
echo -e "   ${GREEN}${MODEL_BUCKET}${NC}"
