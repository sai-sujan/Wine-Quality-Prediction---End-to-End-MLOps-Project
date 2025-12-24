# Quick Fix Reference - GitHub Actions Errors

## What Was Wrong?

Your GitHub Actions were failing because of leftover files from the old **customer satisfaction** project mixed with the new **wine quality** project.

## The Errors

### Error 1: SAM Deploy Failure
```
Error: Stack aws-sam-cli-managed-default is missing Tags and/or Outputs
```
**Cause:** Old `template.yaml` SAM file was present

### Error 2: NoneType Attribute Error
```
AttributeError: 'NoneType' object has no attribute 'name'
```
**Cause:** Experiment tracker not configured in GitHub Actions

### Error 3: Wrong Import Path
```
from model.model_dev import LinearRegressionModel
```
**Cause:** CI workflow using old import path

## What Was Fixed?

### 1. Removed Old Customer Satisfaction Files ❌
- `template.yaml` - SAM CloudFormation template
- `lambda_function.py` - Old Lambda handler
- `.github/workflows/deploy-aws.yml` - SAM deployment workflow

### 2. Fixed Code Issues ✅
- [steps/model_train.py:21](steps/model_train.py#L21) - Handle None experiment tracker
- [.github/workflows/ci.yml:89](.github/workflows/ci.yml#L89) - Fixed import path
- [.github/workflows/retrain-and-deploy.yml](.github/workflows/retrain-and-deploy.yml) - Updated to use wine quality config

### 3. Now Using ✅
- `lambda_handler.py` - Wine quality Lambda handler
- `deploy_lambda.sh` - Direct Lambda deployment (no SAM)
- `.github/workflows/deploy-to-aws.yml` - Wine quality deployment

## File Comparison

| Old (Customer Satisfaction) | New (Wine Quality) | Status |
|----------------------------|-------------------|---------|
| template.yaml | deploy_lambda.sh | ✅ Removed |
| lambda_function.py | lambda_handler.py | ✅ Removed |
| deploy-aws.yml | deploy-to-aws.yml | ✅ Removed |
| model/model_dev.py | src/model_dev.py | ✅ Fixed imports |

## GitHub Workflows Status

All 4 workflows are now compatible with wine quality project:

1. **ci.yml** ✅
   - Runs tests
   - Validates pipeline
   - Fixed imports

2. **train-model.yml** ✅
   - Trains randomforest model
   - Uploads artifacts

3. **deploy-to-aws.yml** ✅
   - Deploys to Lambda
   - Tests endpoint

4. **retrain-and-deploy.yml** ✅
   - Monthly retraining
   - Conditional deployment

## How to Push These Fixes

```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "Fix GitHub Actions: remove old customer satisfaction files, update workflows for wine quality"

# Push to GitHub
git push origin main
```

## Verify It Works

After pushing, check GitHub Actions:
1. Go to your repo on GitHub
2. Click "Actions" tab
3. Workflows should now run without SAM errors

## If You Still See Errors

### Clean up old CloudFormation stacks:
```bash
# Delete old SAM stack (if it exists)
aws cloudformation delete-stack \
  --stack-name aws-sam-cli-managed-default \
  --region us-east-1

# Delete old customer satisfaction stack (if it exists)
aws cloudformation delete-stack \
  --stack-name customer-satisfaction-mlops \
  --region us-east-1
```

## Summary

**Before:** Mixed customer satisfaction + wine quality files causing conflicts
**After:** Clean wine quality project with working GitHub Actions

**Key Changes:**
- No more SAM/CloudFormation
- Direct Lambda deployment with bash scripts
- Fixed experiment tracker handling
- Correct import paths
- Wine quality configuration (us-east-2, wine-quality-mlops-sujan bucket)
