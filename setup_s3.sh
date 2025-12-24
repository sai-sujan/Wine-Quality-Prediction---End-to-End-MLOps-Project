#!/bin/bash
set -e

echo "🪣 Setting up S3 Bucket for MLOps"
echo "=================================="

BUCKET_NAME="wine-quality-mlops-sujan"
REGION="us-east-2"

# Check AWS credentials
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ Error: AWS credentials not configured"
    echo "💡 Run: aws configure"
    exit 1
fi

echo "✅ AWS credentials verified"
echo ""

# Create S3 bucket
echo "📦 Creating S3 bucket: $BUCKET_NAME in $REGION..."
if aws s3 ls "s3://$BUCKET_NAME" 2>/dev/null; then
    echo "✅ Bucket already exists: $BUCKET_NAME"
else
    aws s3 mb "s3://$BUCKET_NAME" --region "$REGION"
    echo "✅ Bucket created: $BUCKET_NAME"
fi

# Enable versioning
echo "🔄 Enabling versioning..."
aws s3api put-bucket-versioning \
    --bucket "$BUCKET_NAME" \
    --versioning-configuration Status=Enabled \
    --region "$REGION"
echo "✅ Versioning enabled"

# Create folder structure
echo "📁 Creating folder structure..."
echo "" | aws s3 cp - "s3://$BUCKET_NAME/models/.keep"
echo "" | aws s3 cp - "s3://$BUCKET_NAME/hyperparameters/.keep"
echo "" | aws s3 cp - "s3://$BUCKET_NAME/logs/.keep"
echo "✅ Folder structure created"

# Set bucket policy for Lambda access (optional)
echo "🔐 Configuring bucket permissions..."
cat > /tmp/bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLambdaAccess",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
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

aws s3api put-bucket-policy \
    --bucket "$BUCKET_NAME" \
    --policy file:///tmp/bucket-policy.json \
    --region "$REGION" || echo "⚠️  Could not set bucket policy (may need additional permissions)"

rm /tmp/bucket-policy.json

echo ""
echo "✅ S3 Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Bucket: s3://$BUCKET_NAME"
echo "🌍 Region: $REGION"
echo "📂 Folders:"
echo "   - models/"
echo "   - hyperparameters/"
echo "   - logs/"
echo ""
echo "Next steps:"
echo "  1. ./train_aws.sh          - Train and upload model"
echo "  2. ./deploy_lambda.sh      - Deploy Lambda function"
