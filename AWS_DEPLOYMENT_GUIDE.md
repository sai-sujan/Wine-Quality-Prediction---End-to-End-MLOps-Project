# AWS Lambda Deployment Guide

Complete guide to deploy your ML model to AWS Lambda for public access.

## 🎯 What You'll Get

After deployment, you'll have:
- **Public API Endpoint**: Anyone can make predictions via HTTPS
- **Serverless**: Pay only for what you use (likely free tier)
- **Scalable**: Automatically handles traffic
- **Professional**: Production-ready ML API

## 📋 Prerequisites

### 1. AWS Account (Free Tier)

1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the signup process (requires credit card, but uses free tier)
4. Free tier includes:
   - 1 million Lambda requests/month (FREE)
   - 1GB API Gateway data transfer (FREE)
   - 5GB S3 storage (FREE)

### 2. Install AWS CLI

**macOS:**
```bash
# Using Homebrew
brew install awscli

# Verify installation
aws --version
```

**Alternative (Python pip):**
```bash
pip install awscli
```

### 3. Install AWS SAM CLI

**macOS:**
```bash
# Using Homebrew
brew install aws-sam-cli

# Verify installation
sam --version
```

## 🚀 Deployment Steps

### Step 1: Configure AWS Credentials

```bash
# Run AWS configure
aws configure

# You'll be prompted for:
# AWS Access Key ID: (from AWS Console → Security Credentials)
# AWS Secret Access Key: (from AWS Console → Security Credentials)
# Default region: us-east-1 (recommended)
# Default output format: json
```

**How to get AWS credentials:**
1. Log into [AWS Console](https://console.aws.amazon.com)
2. Click your name (top right) → "Security Credentials"
3. Scroll to "Access keys"
4. Click "Create access key"
5. Copy both Access Key ID and Secret Access Key

### Step 2: Deploy to AWS

```bash
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project

# Run deployment script
./deploy_aws.sh
```

This will:
1. ✅ Build your Lambda function
2. ✅ Create S3 bucket for models
3. ✅ Deploy API Gateway
4. ✅ Set up all infrastructure
5. ✅ Return your public API URL

**Expected output:**
```
🚀 Deploying Customer Satisfaction Prediction API to AWS Lambda
================================================================
✓ AWS credentials configured
📍 Using AWS Account: 123456789012
📍 Using AWS Region: us-east-1
🔨 Building Lambda function...
📦 Packaging application...
🚀 Deploying to AWS...
✅ Deployment complete!

📊 Stack Outputs:
┌────────────────────┬──────────────────────────────────────┐
│ ApiUrl             │ https://abc123.execute-api.us-east-1 │
│ PredictionEndpoint │ https://abc123.../prod/predict       │
│ ModelBucketName    │ customer-satisfaction-mlops-models   │
└────────────────────┴──────────────────────────────────────┘

🎉 Deployment Successful!
```

### Step 3: Upload Your Model

```bash
# Upload your trained model to S3
./upload_model.sh
```

This uploads your latest MLflow model to AWS S3.

### Step 4: Test Your API

```bash
# Test the deployed API
./test_api.sh
```

**Expected response:**
```json
{
  "prediction": 3.45,
  "customer_satisfaction_score": 3.45,
  "model_version": "v1.0",
  "message": "Prediction successful"
}
```

## 🌐 Share Your Project

After deployment, you'll have a public URL like:
```
https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/predict
```

**Share this URL with:**
- Potential employers
- On your resume/portfolio
- In GitHub README
- LinkedIn posts

## 💰 Cost Estimates

**AWS Free Tier (12 months):**
- Lambda: 1M requests/month FREE
- API Gateway: 1M requests/month FREE
- S3: 5GB storage FREE

**After Free Tier:**
- Lambda: $0.20 per 1M requests
- API Gateway: $3.50 per 1M requests
- S3: $0.023 per GB/month

**For a portfolio project:** Likely stays FREE!

## 🔧 Updating Your Model

When you train a new model:

```bash
# 1. Train new model
python run_deployment.py --config deploy

# 2. Upload to AWS
./upload_model.sh

# 3. Test
./test_api.sh
```

The API automatically uses the latest model!

## 📊 Monitoring

### View Logs

```bash
# View Lambda logs
sam logs --stack-name customer-satisfaction-mlops --tail

# Or in AWS Console:
# CloudWatch → Log Groups → /aws/lambda/customer-satisfaction-mlops-PredictionFunction
```

### Check Metrics

In AWS Console:
1. Go to CloudWatch
2. Select "Metrics"
3. Find your Lambda function
4. View: Invocations, Duration, Errors

## 🐛 Troubleshooting

### Deployment Fails

**Error: "AWS credentials not configured"**
```bash
# Reconfigure AWS
aws configure
```

**Error: "Stack already exists"**
```bash
# Delete existing stack
aws cloudformation delete-stack --stack-name customer-satisfaction-mlops

# Wait for deletion, then deploy again
./deploy_aws.sh
```

### Model Prediction Fails

**Error: "Model not found"**
```bash
# Upload model
./upload_model.sh
```

**Error: "Internal server error"**
```bash
# Check logs
sam logs --stack-name customer-satisfaction-mlops --tail

# Verify model was trained
ls ~/Library/Application\ Support/zenml/local_stores/*/mlruns
```

## 🗑️ Cleanup (Delete Everything)

To avoid any charges:

```bash
# Delete the entire stack
aws cloudformation delete-stack --stack-name customer-satisfaction-mlops

# Delete deployment bucket
aws s3 rb s3://customer-satisfaction-mlops-deployment-$(aws sts get-caller-identity --query Account --output text) --force

# Delete model bucket
aws s3 rb s3://customer-satisfaction-mlops-models-$(aws sts get-caller-identity --query Account --output text) --force
```

## 📖 Architecture Details

```
User Request
    ↓
API Gateway (HTTPS)
    ↓
Lambda Function (Python 3.12)
    ↓
Load Model from S3
    ↓
Make Prediction
    ↓
Return JSON Response
```

**Benefits:**
- ✅ Serverless (no server management)
- ✅ Auto-scaling (handles any traffic)
- ✅ Cost-effective (pay per use)
- ✅ HTTPS by default (secure)
- ✅ Global edge network (fast)

## 🎓 Next Steps

1. **Deploy to AWS**: Run `./deploy_aws.sh`
2. **Test Your API**: Run `./test_api.sh`
3. **Add to Resume**: Link your API endpoint
4. **Push to GitHub**: Share your code
5. **Write Blog Post**: Document your learnings

## 📞 Support

**AWS Free Tier Questions:**
- Check: [aws.amazon.com/free](https://aws.amazon.com/free)

**Technical Issues:**
- AWS Support: [console.aws.amazon.com/support](https://console.aws.amazon.com/support)
- AWS Documentation: [docs.aws.amazon.com](https://docs.aws.amazon.com)

## ✅ Checklist

- [ ] AWS Account created
- [ ] AWS CLI installed and configured
- [ ] AWS SAM CLI installed
- [ ] Model trained locally
- [ ] Deployed to AWS (`./deploy_aws.sh`)
- [ ] Model uploaded (`./upload_model.sh`)
- [ ] API tested (`./test_api.sh`)
- [ ] URL shared on GitHub/Resume

Good luck with your deployment! 🚀
