# AWS Deployment Workflow Guide

## How It Works Now ✅

The **Deploy to AWS** workflow (`.github/workflows/deploy-to-aws.yml`) now runs **automatically** when you push changes to deployment-related files.

## Automatic Triggers

The workflow runs automatically when you push to `main` branch and change any of these files:

- `lambda_handler.py` - Lambda function code
- `src/s3_utils.py` - S3 utilities
- `deploy_lambda.sh` - Lambda deployment script
- `deploy_all.sh` - Complete deployment script
- `setup_s3.sh` - S3 setup script
- `.github/workflows/deploy-to-aws.yml` - The workflow itself

## What Happens on Push

When you push changes to these files, GitHub Actions automatically:

1. **Sets up S3 bucket** - Ensures bucket exists and is configured
2. **Trains the model** - Runs `run_aws.py` to train RandomForest model
3. **Uploads to S3** - Saves model and hyperparameters to S3
4. **Deploys Lambda** - Creates/updates Lambda function with latest code
5. **Tests endpoint** - Makes a test prediction to verify it works
6. **Comments on commit** - Posts Lambda URL as a comment

## Manual Trigger (Optional)

You can also run it manually from GitHub Actions tab:

1. Go to your repo on GitHub
2. Click "Actions" tab
3. Select "Deploy to AWS" workflow
4. Click "Run workflow"
5. Choose options:
   - ✅ Deploy Lambda function (default: yes)
   - ✅ Upload model to S3 (default: yes)

## Current Status

Since we just pushed the workflow update, it **will now trigger automatically** on this push!

Check your GitHub Actions tab to see it running.

## Workflow Steps Breakdown

### Step 1: Setup S3 Bucket
```bash
./setup_s3.sh
```
Creates bucket: `wine-quality-mlops-sujan` in `us-east-2`

### Step 2: Train & Upload Model
```bash
python run_aws.py
```
- Trains RandomForest with hyperparameter tuning
- Saves model.pkl and best_params.json
- Uploads both to S3

### Step 3: Deploy Lambda
```bash
./deploy_lambda.sh
```
- Creates deployment package (handler + scikit-learn)
- Creates/updates Lambda function
- Sets up API Gateway
- Configures IAM roles

### Step 4: Test Endpoint
Makes a POST request to verify Lambda works:
```bash
curl -X POST https://API_ENDPOINT/ \
  -d '{"fixed_acidity":7.4,...}'
```

### Step 5: Comment with URL
Posts the Lambda endpoint URL as a commit comment for easy access.

## Required GitHub Secrets

Make sure these are set in your repo (Settings → Secrets and variables → Actions):

- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key

## Monitoring Deployment

### View Logs
1. Go to GitHub Actions tab
2. Click on the running workflow
3. Click on "Deploy to AWS" job
4. Expand each step to see logs

### Check Lambda Function
```bash
aws lambda get-function --function-name wine-quality-predictor --region us-east-2
```

### View Lambda Logs
```bash
aws logs tail /aws/lambda/wine-quality-predictor --follow --region us-east-2
```

### Test Lambda Locally
```bash
curl -X POST YOUR_LAMBDA_URL \
  -H 'Content-Type: application/json' \
  -d '{"fixed_acidity":7.4,"volatile_acidity":0.7,"citric_acid":0,"residual_sugar":1.9,"chlorides":0.076,"free_sulfur_dioxide":11,"total_sulfur_dioxide":34,"density":0.9978,"pH":3.51,"sulphates":0.56,"alcohol":9.4,"wine_type_encoded":0}'
```

## Troubleshooting

### Workflow Not Running?
- Check that you pushed changes to one of the trigger files
- Verify you're pushing to `main` branch
- Check GitHub Actions tab for any errors

### AWS Credentials Error?
- Verify secrets are set in GitHub repo settings
- Check IAM permissions allow Lambda and S3 operations

### Lambda Deployment Fails?
- Check Lambda package size (should be < 50MB)
- Verify IAM role exists and has correct permissions
- Check CloudWatch Logs for Lambda errors

### Model Not Found in S3?
- Verify S3 bucket was created successfully
- Check training step completed without errors
- Verify model uploaded to `s3://wine-quality-mlops-sujan/models/model.pkl`

## Cost Considerations

### What You'll Pay For:
- **S3 Storage** - ~$0.023/GB/month (model is ~1MB = ~$0.00002/month)
- **Lambda Invocations** - Free tier: 1M requests/month, then $0.20/1M requests
- **Lambda Duration** - Free tier: 400,000 GB-seconds/month
- **API Gateway** - Free tier: 1M requests/month, then $3.50/1M requests

**Estimated Monthly Cost:** ~$0.00 (within free tier for development)

## Next Steps

1. ✅ Workflow is now configured for automatic deployment
2. ✅ Push was successful - check GitHub Actions tab
3. 🔄 Wait for workflow to complete (~5-10 minutes)
4. 📋 Copy Lambda endpoint URL from commit comment
5. 🎨 Update Streamlit dashboard with Lambda URL
6. 🧪 Test predictions through dashboard

## Example: Making Changes

When you update your Lambda code:

```bash
# Edit lambda_handler.py
vim lambda_handler.py

# Commit and push
git add lambda_handler.py
git commit -m "Update Lambda handler"
git push

# GitHub Actions automatically deploys! ✨
```

No manual deployment needed - just push your code!
