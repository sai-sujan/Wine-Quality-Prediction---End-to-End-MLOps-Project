# Cleanup Summary - Customer Satisfaction to Wine Quality Migration

## Files Removed

These old customer satisfaction project files were removed to prevent conflicts:

### 1. AWS SAM Deployment Files
- **template.yaml** - SAM CloudFormation template for customer satisfaction
  - Defined resources for old project (customer-satisfaction-mlops)
  - Used different S3 bucket naming convention
  - Region: us-east-1 (old) vs us-east-2 (new)

### 2. Old Lambda Handler
- **lambda_function.py** - Customer satisfaction prediction Lambda
  - Used customer satisfaction features (payment_*, product_*, freight_value)
  - Different model loading mechanism (MLflow from S3)
  - Different API contract

### 3. Old GitHub Workflow
- **.github/workflows/deploy-aws.yml** - SAM-based deployment
  - Used `sam build` and `sam deploy`
  - CloudFormation stack management
  - Wrong region and stack name

## Current Wine Quality Files

These are the active files for the wine quality project:

### Lambda Deployment
- **lambda_handler.py** - Wine quality prediction handler
  - Features: fixed_acidity, volatile_acidity, citric_acid, etc.
  - Direct S3 model loading with pickle
  - Region: us-east-2

### Deployment Scripts
- **deploy_lambda.sh** - Direct Lambda deployment
  - No SAM/CloudFormation
  - Minimal package with scikit-learn
  - Function name: wine-quality-predictor

- **deploy_all.sh** - Complete deployment pipeline
  - S3 setup → Model training → Lambda deployment

### GitHub Workflows
- **.github/workflows/deploy-to-aws.yml** - Wine quality deployment
- **.github/workflows/train-model.yml** - Model training
- **.github/workflows/retrain-and-deploy.yml** - Automated retraining
- **.github/workflows/ci.yml** - CI/CD validation

## Why These Files Were Removed

### SAM Template Issue
The SAM error you saw:
```
Error: Stack aws-sam-cli-managed-default is missing Tags and/or Outputs
```

This happened because:
1. GitHub Actions found `template.yaml` in the repo
2. Old workflow tried to run `sam deploy` 
3. SAM looked for a stack that doesn't exist anymore
4. The stack was in ROLLBACK_COMPLETE state from a previous failed deployment

### Lambda Function Conflict
Having both `lambda_function.py` and `lambda_handler.py` could cause:
- Wrong handler being packaged in deployment
- Import confusion
- Different feature schemas causing prediction errors

### Workflow Conflict
The old `deploy-aws.yml` was triggering on certain file changes and trying to deploy using SAM instead of your new bash scripts.

## Migration Checklist ✓

- [x] Removed old SAM template
- [x] Removed old Lambda function
- [x] Removed old deployment workflow
- [x] Updated CI workflow imports
- [x] Fixed experiment tracker NoneType error
- [x] Updated retrain-and-deploy workflow
- [x] Created comprehensive tests

## Next Steps

1. **Commit and push these changes**:
   ```bash
   git add .
   git commit -m "Remove old customer satisfaction files, fix GitHub Actions workflows"
   git push
   ```

2. **Verify workflows run successfully** in GitHub Actions tab

3. **Test Lambda deployment** locally:
   ```bash
   ./deploy_all.sh
   ```

4. **Clean up AWS resources** (optional):
   If there are old CloudFormation stacks, delete them:
   ```bash
   aws cloudformation delete-stack --stack-name customer-satisfaction-mlops --region us-east-1
   aws cloudformation delete-stack --stack-name aws-sam-cli-managed-default --region us-east-1
   ```

## Configuration Differences

| Aspect | Customer Satisfaction (Old) | Wine Quality (New) |
|--------|---------------------------|-------------------|
| Region | us-east-1 | us-east-2 |
| Stack Name | customer-satisfaction-mlops | N/A (no stack) |
| Function Name | PredictionFunction (SAM) | wine-quality-predictor |
| Bucket | `${StackName}-models-${AccountId}` | wine-quality-mlops-sujan |
| Handler | lambda_function.py | lambda_handler.py |
| Deployment | SAM CLI | Bash script |
| Features | 12 (payment, product data) | 12 (wine chemistry) |
| Model Format | MLflow | Pickle |

