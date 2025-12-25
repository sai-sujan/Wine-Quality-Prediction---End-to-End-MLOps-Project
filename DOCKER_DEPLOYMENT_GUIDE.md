# Docker-based Lambda Deployment Guide

## Why Docker?

The Lambda Layer approach was causing dependency issues with scipy modules. Docker containerization is the **AWS-recommended approach** for ML models on Lambda because:

- ✅ No 250MB size limit
- ✅ All dependencies work correctly
- ✅ Easier to maintain
- ✅ Industry best practice

## Architecture

```
Docker Image (ECR) → Lambda Function → API Gateway → Public Endpoint
```

**Components:**
- **Dockerfile**: Builds image with Python 3.12, sklearn, scipy, numpy, joblib
- **ECR (Elastic Container Registry)**: Stores the Docker image
- **Lambda**: Runs the containerized function
- **API Gateway**: Exposes HTTP endpoint

## Deployment Options

### Option 1: GitHub Actions (Recommended)

**Prerequisites:**
1. Ensure your AWS IAM user has ECR permissions (see [AWS_ECR_PERMISSIONS.md](AWS_ECR_PERMISSIONS.md))
2. The managed policy `AmazonEC2ContainerRegistryFullAccess` is the quickest way

**Steps:**
1. Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/deploy-to-aws.yml
2. Click "Run workflow"
3. Select branch: `main`
4. Click "Run workflow"

The workflow will:
- Setup S3 bucket
- Train and upload model
- Build Docker image
- Push to ECR
- Deploy/update Lambda function
- Setup API Gateway
- Test the endpoint
- Comment with the endpoint URL

### Option 2: Local Deployment

**Prerequisites:**
1. Install Docker Desktop
2. Install AWS CLI: `brew install awscli` (macOS) or equivalent
3. Configure AWS credentials: `aws configure`
4. Ensure your AWS user has ECR permissions

**Steps:**
```bash
# Run the deployment script
./deploy_lambda_docker.sh
```

This will:
1. Create ECR repository (if needed)
2. Build Docker image for Linux/AMD64
3. Login to ECR
4. Push image to ECR
5. Create/update Lambda function
6. Setup API Gateway
7. Output the endpoint URL

## Testing

After deployment, test with:

```bash
curl -X POST https://YOUR_API_ENDPOINT \
  -H 'Content-Type: application/json' \
  -d '{"fixed_acidity":7.4,"volatile_acidity":0.7,"citric_acid":0,"residual_sugar":1.9,"chlorides":0.076,"free_sulfur_dioxide":11,"total_sulfur_dioxide":34,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4,"wine_type_encoded":0}'
```

Expected response:
```json
{
  "prediction": 5,
  "model_used": "RandomForest"
}
```

## Troubleshooting

### Error: "User not authorized to perform: ecr:GetAuthorizationToken"

**Fix**: Add ECR permissions to your AWS IAM user
- Easiest: Attach `AmazonEC2ContainerRegistryFullAccess` policy
- Or: Add custom ECR policy from [AWS_ECR_PERMISSIONS.md](AWS_ECR_PERMISSIONS.md)

### Error: Docker daemon not running

**Fix**: Start Docker Desktop

### Error: No module named 'scipy'

This should NOT happen with Docker deployment. If it does:
1. Rebuild the image: `docker build --no-cache --platform linux/amd64 -t wine-quality-lambda:latest .`
2. Verify requirements.txt includes scipy
3. Redeploy

## Files Overview

- **Dockerfile**: Defines the container image
- **deploy_lambda_docker.sh**: Deployment script for ECR + Lambda
- **lambda_handler.py**: Lambda function code
- **requirements.txt**: Python dependencies
- **.github/workflows/deploy-to-aws.yml**: GitHub Actions workflow

## Cost Considerations

- **ECR Storage**: ~$0.10/GB/month for Docker images
- **Lambda**: First 1M requests/month free, then $0.20 per 1M
- **API Gateway**: First 1M requests free, then $1.00 per 1M
- **S3**: Minimal cost for model storage

For this project: **~$1-2/month** at moderate usage.

## Next Steps

1. ✅ Switch to Docker deployment
2. ✅ Ensure AWS user has ECR permissions
3. ✅ Trigger GitHub Actions workflow
4. ✅ Test the endpoint
5. 🎯 Update Streamlit dashboard with new endpoint

## Rollback

If you need to rollback to a previous version:

```bash
# List image tags
aws ecr list-images --repository-name wine-quality-lambda --region us-east-2

# Update Lambda to use a specific image
aws lambda update-function-code \
  --function-name wine-quality-predictor \
  --image-uri YOUR_ACCOUNT.dkr.ecr.us-east-2.amazonaws.com/wine-quality-lambda:TAG \
  --region us-east-2
```
