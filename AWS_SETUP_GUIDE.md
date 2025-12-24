# 🚀 AWS S3 + Lambda Setup Guide

## Overview

This guide will help you set up:
1. ✅ **S3 Bucket** - Store models, hyperparameters, and logs
2. ✅ **AWS Lambda** - Serverless model deployment
3. ✅ **API Gateway** - HTTP endpoint for predictions

---

## Prerequisites You'll Need

### 1. AWS Account
- Sign up at: https://aws.amazon.com/free/
- Free tier includes:
  - 5GB S3 storage (free for 12 months)
  - 1 million Lambda requests/month (always free)

### 2. AWS CLI Installation

**Check if installed:**
```bash
aws --version
```

**Install if needed:**

**macOS:**
```bash
brew install awscli
```

**Windows:**
```bash
# Download from: https://aws.amazon.com/cli/
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### 3. AWS SAM CLI (for Lambda deployment)

**macOS:**
```bash
brew install aws-sam-cli
```
a
**Windows/Linux:**
See: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

---

## Step-by-Step Setup

### Step 1: Get AWS Credentials

1. **Login to AWS Console**: https://console.aws.amazon.com/

2. **Navigate to IAM**:
   - Search for "IAM" in the top search bar
   - Click "Users" in the left sidebar
   - Click your username (or create a new user)

3. **Create Access Key**:
   - Click "Security credentials" tab
   - Scroll to "Access keys"
   - Click "Create access key"
   - Choose "CLI" as use case
   - Download or copy:
     - ✅ Access Key ID (looks like: `AKIAIOSFODNN7EXAMPLE`)
     - ✅ Secret Access Key (looks like: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

   ⚠️ **IMPORTANT**: Save these somewhere safe! You can't see the Secret Key again.

### Step 2: Configure AWS CLI

Run this command and enter your credentials:

```bash
aws configure
```

**Prompts and Answers:**
```
AWS Access Key ID: [paste your Access Key ID]
AWS Secret Access Key: [paste your Secret Access Key]
Default region name: us-east-1  # or your preferred region
Default output format: json
```

**Verify it works:**
```bash
aws sts get-caller-identity
```

Should show:
```json
{
    "UserId": "AIDAI...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

### Step 3: Choose Your S3 Bucket Name

**Requirements:**
- Must be globally unique across all AWS
- Only lowercase letters, numbers, hyphens
- 3-63 characters

**Suggestions:**
- `wine-quality-mlops-yourname`
- `mlops-wine-project-yourname`
- `yourname-wine-quality-prod`

**📝 Write down your choice:**
```
MY_BUCKET_NAME: _________________________________
```

### Step 4: Choose Your AWS Region

**Common regions:**
- `us-east-1` - US East (N. Virginia) - Default, cheapest
- `us-west-2` - US West (Oregon)
- `eu-west-1` - Europe (Ireland)
- `ap-south-1` - Asia Pacific (Mumbai)

**📝 Write down your choice:**
```
MY_REGION: _________________________________
```

---

## What Will Happen Next


### 1. Create S3 Bucket Setup Script
```bash
./setup_s3.sh
```
This will:
- Create S3 bucket with your chosen name
- Set up folder structure:
  ```
  s3://your-bucket/
  ├── models/           # Trained models
  ├── hyperparameters/  # best_params.json
  ├── logs/            # Training & prediction logs
  └── mlflow/          # MLflow artifacts
  ```
- Configure bucket permissions
- Enable versioning (keep model history)

### 2. Update Pipeline Code

**Automatic S3 Upload After Training:**
```python
# After model training completes:
✅ Upload model.pkl → s3://bucket/models/wine-quality-v1.pkl
✅ Upload best_params.json → s3://bucket/hyperparameters/
✅ Upload training logs → s3://bucket/logs/
```

**Automatic S3 Download for Predictions:**
```python
# API/Lambda automatically loads from:
✅ Latest model from S3
✅ Cached hyperparameters from S3
```

### 3. Lambda Deployment

**One-command deployment:**
```bash
./deploy_lambda.sh
```

This creates:
- Lambda function with your model
- API Gateway endpoint
- Returns: `https://abc123.execute-api.us-east-1.amazonaws.com/prod/predict`

### 4. Files I'll Create for You

```
fcc_mlops_project/
├── setup_s3.sh                 # Create & configure S3 bucket
├── deploy_lambda.sh            # Deploy to AWS Lambda
├── s3_config.py                # S3 upload/download utilities
├── lambda_s3.py               # Lambda handler with S3 integration
└── AWS_DEPLOYMENT_GUIDE.md    # Step-by-step deployment instructions
```

---

## Cost Estimate

### Free Tier (First 12 Months)
- ✅ S3: 5GB storage - **FREE**
- ✅ Lambda: 1M requests/month - **FREE**
- ✅ API Gateway: 1M calls/month - **FREE**

### After Free Tier
- S3: ~$0.023/GB/month (~$0.02/month for your model)
- Lambda: $0.20 per 1M requests
- API Gateway: $3.50 per 1M requests

**Estimated cost:** Less than $0.50/month for low traffic

---

## Security Best Practices

### 1. IAM User Permissions

Your user should have these policies:
- ✅ `AmazonS3FullAccess` (or custom S3 policy)
- ✅ `AWSLambda_FullAccess`
- ✅ `IAMFullAccess` (to create Lambda execution role)
- ✅ `AmazonAPIGatewayAdministrator`

### 2. Don't Commit Credentials

**Already configured in `.gitignore`:**
```
.aws/
credentials
*.pem
*.key
```

### 3. Use Environment Variables

I'll set up your code to use:
```python
import os
AWS_BUCKET = os.getenv('AWS_BUCKET_NAME', 'your-bucket-name')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
```

---

## Quick Start (Copy & Fill)

**Please provide these details:**

```yaml
# Your AWS Configuration
AWS_ACCESS_KEY_ID: _____________________ # From Step 1
AWS_SECRET_ACCESS_KEY: _________________ # From Step 1
AWS_REGION: ____________________________ # e.g., us-east-1
S3_BUCKET_NAME: ________________________ # Must be globally unique

# Optional (I'll use defaults if not provided)
LAMBDA_FUNCTION_NAME: wine-quality-predictor  # Keep default or change
API_NAME: Wine-Quality-API                     # Keep default or change
```

---

## Alternative: I'll Set Up Test Bucket

If you want me to just set up a demo/test configuration:

**I can create placeholder scripts that:**
- Use mock S3 bucket names (you replace with real ones later)
- Show you exactly what commands to run
- Include troubleshooting for common issues

Just say: **"Create demo setup"** and I'll proceed with example values.

---

## Next Steps

**Option 1: Full Setup (Recommended)**
Provide the details above, and I'll create all the scripts and code.

**Option 2: Demo/Practice Setup**
I'll create scripts with placeholder values you can test with.

**Option 3: Manual Walkthrough**
I'll create step-by-step instructions, you run each command yourself.

Which option do you prefer? 🚀
