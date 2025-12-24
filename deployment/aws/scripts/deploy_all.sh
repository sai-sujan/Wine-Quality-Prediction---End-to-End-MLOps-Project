#!/bin/bash
set -e

echo "🚀 Complete AWS MLOps Deployment"
echo "================================="
echo ""

# Step 1: Setup S3
echo "📦 Step 1/3: Setting up S3 bucket..."
./deployment/aws/scripts/setup_s3.sh
echo ""

# Step 2: Train and upload model
echo "🧠 Step 2/3: Training model and uploading to S3..."
./deployment/aws/scripts/train_aws.sh
echo ""

# Step 3: Deploy Lambda
echo "⚡ Step 3/3: Deploying Lambda function with Layer..."
./deployment/aws/scripts/deploy_lambda_with_layer.sh
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Complete Deployment Finished!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Your MLOps pipeline is now fully deployed to AWS!"
echo ""
echo "📊 Resources created:"
echo "   • S3 Bucket: s3://wine-quality-mlops-sujan"
echo "   • Lambda Function: wine-quality-predictor"
echo "   • API Gateway: HTTP API"
echo ""
echo "🎯 Next steps:"
echo "   1. Copy the Lambda endpoint URL from above"
echo "   2. Open Streamlit dashboard: streamlit run src/dashboard/streamlit_app.py"
echo "   3. Switch to 'AWS Lambda' mode in sidebar"
echo "   4. Paste the endpoint URL"
echo "   5. Start making predictions!"
