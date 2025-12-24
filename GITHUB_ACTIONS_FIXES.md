# GitHub Actions Fixes

## Issues Fixed

### 1. Experiment Tracker NoneType Error

**Problem:**
```
AttributeError: 'NoneType' object has no attribute 'name'
```

**Root Cause:**
In `steps/model_train.py` and `steps/evaluation.py`, the code was trying to access `.name` on the experiment tracker when it might be `None` (when MLflow isn't configured in GitHub Actions).

**Fix:**
Changed in both files:

**steps/model_train.py (line 21):**
```python
# Before
@step(experiment_tracker=experiment_tracker.name)

# After
@step(experiment_tracker=experiment_tracker.name if experiment_tracker else None)
```

**steps/evaluation.py (line 12):**
```python
# Before
@step(experiment_tracker = experiment_tracker.name)

# After
@step(experiment_tracker = experiment_tracker.name if experiment_tracker else None)
```

This safely handles the case when no experiment tracker is configured.

---

### 2. Old SAM Deployment Workflow

**Problem:**
The `deploy-aws.yml` workflow was using AWS SAM CLI with old customer-satisfaction settings:
- Stack name: `customer-satisfaction-mlops`
- Region: `us-east-1`
- Using `template.yaml` (SAM template)
- Trying to deploy with SAM instead of Lambda direct deployment

**Fix:**
Deleted old customer satisfaction files:
- `.github/workflows/deploy-aws.yml` - Old SAM deployment workflow
- `template.yaml` - SAM CloudFormation template
- `lambda_function.py` - Old customer satisfaction Lambda handler

Now using wine quality files:
- `.github/workflows/deploy-to-aws.yml` - Uses `deploy_lambda.sh` script
- `lambda_handler.py` - Wine quality Lambda handler
- Direct Lambda deployment without SAM

---

### 3. Updated Retrain-and-Deploy Workflow

**File:** `.github/workflows/retrain-and-deploy.yml`

**Changes Made:**

1. **Updated default model** from `LinearRegressionModel` to `randomforest`:
   ```yaml
   # Line 9
   default: 'randomforest'

   # Line 11-15 - Reordered options
   options:
     - randomforest
     - lightgbm
     - xgboost
     - LinearRegressionModel
   ```

2. **Updated training command** to use new script:
   ```yaml
   # Line 57
   python run_local.py  # Changed from run_pipeline.py
   ```

3. **Replaced SAM deployment** with Lambda deployment:
   ```yaml
   # Lines 118-121 - Removed SAM, added deploy_all.sh
   - name: Deploy to AWS Lambda
     run: |
       chmod +x deploy_all.sh
       ./deploy_all.sh
   ```

4. **Updated AWS region** to `us-east-2` (wine quality bucket region)

5. **Removed SAM-specific steps**:
   - Setup AWS SAM
   - sam build
   - sam deploy
   - CloudFormation stack queries

---

### 4. Fixed CI Workflow Model Import

**Problem:**
In `.github/workflows/ci.yml`, line 89 was importing from old `model.model_dev` path:
```python
from model.model_dev import LinearRegressionModel
```

**Fix:**
Updated to use correct `src.model_dev` path and added RandomForestModel:
```python
from src.model_dev import LinearRegressionModel, RandomForestModel
```

---

## Current GitHub Workflows

### 1. train-model.yml
- Trains model locally
- Default: randomforest
- Uploads artifacts (model.pkl, best_params.json)

### 2. deploy-to-aws.yml
- Sets up S3 bucket
- Trains and uploads model to S3
- Deploys Lambda function
- Tests Lambda endpoint

### 3. retrain-and-deploy.yml
- Trains model
- Evaluates MSE threshold
- Conditionally deploys to AWS Lambda
- Creates GitHub release

### 4. ci.yml
- Validates code structure
- Runs pipeline validation

---

## Testing the Fixes

Run these commands locally to verify:

```bash
# Test imports work
python3 -c "from pipelines.training_pipeline import train_pipeline; print('✓ OK')"

# Test local training
python run_local.py

# Test AWS deployment (requires AWS credentials)
./deploy_all.sh
```

---

## What Changed in Deployment

### Before (Customer Satisfaction)
- AWS SAM CLI
- CloudFormation stacks
- template.yaml configuration
- us-east-1 region
- Stack name: customer-satisfaction-mlops

### After (Wine Quality)
- Direct Lambda deployment
- deploy_lambda.sh bash script
- us-east-2 region
- Function name: wine-quality-predictor
- Bucket: wine-quality-mlops-sujan

---

## Next Steps

1. Push these changes to GitHub
2. GitHub Actions should now run successfully
3. Test the workflows manually via "Actions" tab
4. Monitor deployment logs for any issues
