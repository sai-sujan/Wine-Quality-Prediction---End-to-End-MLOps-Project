# CI/CD Setup Guide

Complete guide to set up automated training and deployment for your MLOps project.

## 🎯 What You'll Get

After setup:
- ✅ **Automatic testing** on every code push
- ✅ **Scheduled model retraining** (weekly/monthly)
- ✅ **Auto-deployment to AWS** when code changes
- ✅ **Smart deployment** - only deploys if model performs well
- ✅ **GitHub releases** for model versions
- ✅ **Deployment summaries** and notifications

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **AWS Account** (free tier)
3. **Your code pushed to GitHub**

## 🚀 Step-by-Step Setup

### Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project
git init

# Add all files
git add .

# Create .gitignore to exclude unnecessary files
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
zenml_env/
venv/
env/

# ZenML
.zenml/
*.db

# MLflow
mlruns/
mlartifacts/

# AWS
.aws-sam/
packaged.yaml

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.pem
*.key
EOF

# Commit
git add .gitignore
git commit -m "Initial commit: MLOps project with CI/CD"

# Create GitHub repo and push
# Go to github.com and create new repository
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/mlops-customer-satisfaction.git
git branch -M main
git push -u origin main
```

### Step 2: Configure GitHub Secrets

1. **Go to your GitHub repository**
   - Navigate to: `https://github.com/YOUR_USERNAME/mlops-customer-satisfaction`

2. **Access Secrets Settings**
   - Click **Settings** (top menu)
   - Sidebar → **Secrets and variables** → **Actions**

3. **Add AWS Credentials**

   Click **New repository secret** and add:

   **Secret 1: AWS_ACCESS_KEY_ID**
   ```
   Name: AWS_ACCESS_KEY_ID
   Value: <Your AWS Access Key>
   ```

   **Secret 2: AWS_SECRET_ACCESS_KEY**
   ```
   Name: AWS_SECRET_ACCESS_KEY
   Value: <Your AWS Secret Key>
   ```

   **Secret 3: AWS_REGION**
   ```
   Name: AWS_REGION
   Value: us-east-1
   ```

   **How to get AWS credentials:**
   - Log into [AWS Console](https://console.aws.amazon.com)
   - Click your name → **Security Credentials**
   - **Access keys** → **Create access key**
   - Choose **Application running outside AWS**
   - Copy both keys

4. **(Optional) Add MLflow Tracking URI**
   ```
   Name: MLFLOW_TRACKING_URI
   Value: https://your-mlflow-server.com
   ```

### Step 3: Enable GitHub Actions

1. **Go to Actions Tab**
   - Click **Actions** in your repository

2. **Enable Workflows**
   - If prompted, click **I understand my workflows, go ahead and enable them**

3. **Verify Workflows**
   - You should see 4 workflows:
     - CI - Test and Validate
     - Train Model
     - Deploy to AWS
     - Retrain and Deploy

### Step 4: Test Your CI/CD

#### Test 1: Automatic CI

```bash
# Make a small change
echo "# MLOps Project" >> README.md

# Commit and push
git add README.md
git commit -m "Test CI pipeline"
git push origin main
```

**Expected:** CI workflow runs automatically
- Go to **Actions** tab
- See "CI - Test and Validate" running
- All checks should pass ✅

#### Test 2: Manual Model Training

1. Go to **Actions** tab
2. Click **Train Model** workflow
3. Click **Run workflow** (right side)
4. Select options:
   - Model: LinearRegressionModel
   - Fine tuning: false
5. Click **Run workflow**

**Expected:**
- Workflow runs and trains model
- Artifacts uploaded (trained-model, training-metrics)
- Check **Summary** for results

#### Test 3: Deploy to AWS

1. Go to **Actions** tab
2. Click **Deploy to AWS** workflow
3. Click **Run workflow**
4. Select environment: production
5. Click **Run workflow**

**Expected:**
- Lambda function deployed
- API Gateway created
- API URL in deployment summary
- Deployment status: ✅ Success

## 🔄 Automated Workflows Explained

### 1. CI Pipeline (Runs on Every Push)

**File:** `.github/workflows/ci.yml`

**Triggers:** Push to main/develop, Pull Requests

**What it does:**
```
Code Push → Run Tests → Check Formatting → Lint Code →
Security Scan → Validate Pipelines → Report Results
```

**Use case:** Catch bugs before they reach production

### 2. Scheduled Model Training

**File:** `.github/workflows/train-model.yml`

**Triggers:**
- Manual (anytime)
- Weekly (Sundays 00:00 UTC)

**What it does:**
```
Trigger → Load Data → Train Model → Track with MLflow →
Upload Artifacts → Save Metrics
```

**Use case:** Keep model fresh with latest data

### 3. Auto-Deploy on Code Change

**File:** `.github/workflows/deploy-aws.yml`

**Triggers:**
- Push to main (when deployment files change)
- Manual trigger

**What it does:**
```
Code Push → Build SAM App → Deploy to AWS Lambda →
Create API Gateway → Test API → Report URL
```

**Use case:** Automatic deployment when you update code

### 4. Smart Retrain & Deploy

**File:** `.github/workflows/retrain-and-deploy.yml`

**Triggers:**
- Manual (anytime)
- Monthly (1st of month 00:00 UTC)

**What it does:**
```
Trigger → Train Model → Evaluate (MSE) →
If MSE < Threshold → Deploy to AWS → Create Release
If MSE ≥ Threshold → Skip Deployment → Notify
```

**Use case:** Automated monthly model updates with quality gate

## 📊 Monitoring Your CI/CD

### View Workflow Status

```
GitHub Repo → Actions Tab → See all runs

Recent runs show:
✅ CI - Test and Validate (2m ago) - Success
✅ Deploy to AWS (10m ago) - Success
⏳ Train Model (running...)
❌ Retrain and Deploy (1h ago) - Failed
```

### Check Deployment Summary

1. Click on completed workflow run
2. View **Summary** section
3. See:
   - API URL
   - Deployment status
   - Test results
   - Metrics

### Download Artifacts

1. Click completed "Train Model" run
2. Scroll to **Artifacts** section
3. Download:
   - `trained-model` (model files)
   - `training-metrics` (performance data)

## 🎛️ Customize Workflows

### Change Training Schedule

Edit `.github/workflows/train-model.yml`:

```yaml
on:
  schedule:
    # Current: Weekly on Sundays
    - cron: '0 0 * * 0'

    # Daily at midnight:
    - cron: '0 0 * * *'

    # Every 6 hours:
    - cron: '0 */6 * * *'
```

### Change Deployment Threshold

Edit `.github/workflows/retrain-and-deploy.yml`:

```yaml
deploy_threshold:
  description: 'Maximum MSE to deploy'
  default: '5.0'  # Change this value
```

### Add More Models

Edit `.github/workflows/train-model.yml`:

```yaml
model_name:
  options:
    - LinearRegressionModel
    - lightgbm
    - xgboost
    - randomforest
    - YourNewModel  # Add here
```

## 🔔 Notifications

### Slack Notifications (Optional)

Add to your workflows:

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email Notifications

GitHub sends emails automatically for:
- Failed workflows
- Completed workflow runs (if enabled in settings)

**Enable:**
Settings → Notifications → Actions → Choose preferences

## 📈 Best Practices

### 1. Branch Protection

Protect `main` branch:
- Settings → Branches → Add rule
- Require PR reviews before merging
- Require status checks to pass (CI)

### 2. Environment Protection

Settings → Environments → production:
- ✅ Required reviewers (manual approval for prod)
- ✅ Wait timer (delay before deployment)

### 3. Secrets Management

- Never commit secrets to code
- Rotate AWS keys every 90 days
- Use separate AWS accounts for staging/production

### 4. Monitoring

- Check workflow runs daily
- Review failed runs immediately
- Monitor AWS costs in AWS Console

## 🐛 Troubleshooting

### Workflow Stuck on "Queued"

**Cause:** GitHub Actions runner not available (free tier limits)

**Solution:**
- Wait a few minutes
- Or upgrade to paid GitHub plan

### "AWS credentials not found"

**Cause:** Secrets not configured correctly

**Solution:**
```bash
# Verify secrets exist
# Go to Settings → Secrets → Actions
# Check: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

# Test AWS CLI locally
aws sts get-caller-identity
```

### Deployment succeeds but API returns 500

**Cause:** Model not uploaded to S3

**Solution:**
```bash
# Manually upload model
./upload_model.sh

# Or check workflow logs
# Actions → Deploy to AWS → View logs → "Upload model to S3" step
```

### CI fails on "Module not found"

**Cause:** Missing dependency in requirements.txt

**Solution:**
```bash
# Add missing package to requirements.txt
echo "missing-package==1.0.0" >> requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

## 🎓 Next Level

### Add Model Monitoring

Track model drift and performance:
- Integrate with [Evidently](https://www.evidentlyai.com/)
- Set up alerts for performance degradation

### Multi-Stage Deployment

Deploy to staging → test → deploy to production:
- Create staging environment
- Add approval gates
- Run integration tests

### A/B Testing

Deploy multiple model versions:
- Route traffic between models
- Compare performance
- Gradually roll out winners

## ✅ Setup Checklist

- [ ] Code pushed to GitHub
- [ ] AWS credentials configured in GitHub Secrets
- [ ] GitHub Actions enabled
- [ ] CI workflow passing
- [ ] Manual model training tested
- [ ] AWS deployment successful
- [ ] API endpoint working
- [ ] Scheduled workflows configured
- [ ] Notifications set up
- [ ] Documentation updated

## 🎉 You're All Set!

Your CI/CD pipeline is now fully automated!

**What happens now:**
1. Push code → CI runs automatically
2. Weekly → Model retrains automatically
3. Monthly → Model retrains and deploys (if good enough)
4. Any time → Manually trigger training or deployment

**Your project now has:**
- ✅ Professional CI/CD pipeline
- ✅ Automated testing
- ✅ Continuous deployment
- ✅ Model versioning
- ✅ Quality gates

Perfect for your portfolio! 🚀

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Workflow Examples](.github/workflows/README.md)
