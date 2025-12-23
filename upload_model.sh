#!/bin/bash
set -e

echo "📤 Uploading trained model to AWS S3"
echo "====================================="

# Get stack outputs
STACK_NAME="customer-satisfaction-mlops"
AWS_REGION=$(aws configure get region || echo "us-east-1")

MODEL_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`ModelBucketName`].OutputValue' \
    --output text 2>/dev/null)

if [ -z "$MODEL_BUCKET" ]; then
    echo "❌ Stack not deployed. Run ./deploy_aws.sh first"
    exit 1
fi

echo "📦 Model bucket: $MODEL_BUCKET"

# Find the latest MLflow model
MLFLOW_DIR="$HOME/Library/Application Support/zenml/local_stores/b368042e-441e-457a-92a6-cd3abc06cd3a/mlruns"

if [ ! -d "$MLFLOW_DIR" ]; then
    echo "❌ MLflow directory not found"
    exit 1
fi

# Find latest model run
LATEST_RUN=$(find "$MLFLOW_DIR" -name "model" -type d | sort -r | head -1)

if [ -z "$LATEST_RUN" ]; then
    echo "❌ No model found. Train a model first using: python run_deployment.py --config deploy"
    exit 1
fi

echo "📍 Found model: $LATEST_RUN"

# Upload model to S3
echo "⬆️  Uploading model to S3..."
aws s3 cp "$LATEST_RUN" "s3://$MODEL_BUCKET/models/production/model/" --recursive --region ${AWS_REGION}

echo "✅ Model uploaded successfully!"
echo ""
echo "🎯 Your API is now ready to serve predictions!"
echo "Test it with: ./test_api.sh"
