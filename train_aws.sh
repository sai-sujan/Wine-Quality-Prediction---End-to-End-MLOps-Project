#!/bin/bash
set -e

echo "☁️  AWS Training - Model saved to S3"
echo "===================================="

# Activate virtual environment if it exists
if [ -d "zenml_env" ]; then
    source zenml_env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ Error: AWS credentials not configured"
    echo "💡 Run: aws configure"
    exit 1
fi

echo "✅ AWS credentials found"
echo "☁️  Bucket: wine-quality-mlops-sujan"
echo "☁️  Region: us-east-2"
echo ""
echo "📦 Training model with S3 storage..."
echo "☁️  Model will be uploaded to s3://wine-quality-mlops-sujan/models/"
echo "☁️  Parameters will be uploaded to s3://wine-quality-mlops-sujan/hyperparameters/"
echo ""

python run_aws.py

echo ""
echo "✅ AWS training complete!"
echo "☁️  Model uploaded to S3"
echo ""
echo "Next steps:"
echo "  ./deploy_aws.sh      - Deploy to AWS Lambda"
