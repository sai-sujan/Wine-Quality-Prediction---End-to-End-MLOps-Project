# GitHub Actions CI/CD Workflows

This directory contains automated workflows for continuous integration and deployment.

## 🔄 Workflows

### 1. CI - Test and Validate (`ci.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`

**What it does:**
- ✅ Runs unit tests
- ✅ Checks code formatting (Black)
- ✅ Lints code (Flake8)
- ✅ Validates ML pipelines
- ✅ Security scanning
- ✅ Uploads coverage reports

### 2. Train Model (`train-model.yml`)

**Triggers:**
- Manual trigger (workflow_dispatch)
- Weekly schedule (Sundays at 00:00 UTC)

**What it does:**
- ✅ Trains ML model with specified configuration
- ✅ Tracks experiments with MLflow
- ✅ Uploads model artifacts
- ✅ Posts results to PR comments

**Manual trigger options:**
- Model type: LinearRegression, LightGBM, XGBoost, RandomForest
- Enable/disable hyperparameter tuning

### 3. Deploy to AWS (`deploy-aws.yml`)

**Triggers:**
- Push to `main` (only when deployment files change)
- Manual trigger (workflow_dispatch)

**What it does:**
- ✅ Builds AWS SAM application
- ✅ Deploys Lambda function
- ✅ Sets up API Gateway
- ✅ Uploads model to S3
- ✅ Tests deployed API
- ✅ Creates deployment summary

### 4. Retrain and Deploy (`retrain-and-deploy.yml`)

**Triggers:**
- Manual trigger (workflow_dispatch)
- Monthly schedule (1st of month at 00:00 UTC)

**What it does:**
- ✅ Trains new model
- ✅ Evaluates performance
- ✅ Deploys if MSE < threshold
- ✅ Creates GitHub release
- ✅ Sends notifications

**Features:**
- Configurable MSE threshold
- Automated deployment decision
- Model versioning with releases

## 🔐 Required Secrets

Configure these in GitHub repository settings (Settings → Secrets and variables → Actions):

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key | AKIAIOSFODNN7EXAMPLE |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| `AWS_REGION` | AWS region | us-east-1 |
| `MLFLOW_TRACKING_URI` | MLflow tracking server (optional) | https://your-mlflow-server.com |

## 📝 Setup Instructions

### 1. Fork/Clone Repository

```bash
git clone https://github.com/your-username/fcc_mlops_project.git
cd fcc_mlops_project
```

### 2. Configure GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret from the table above

### 3. Enable GitHub Actions

1. Go to **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**

### 4. Test Workflows

**Option A: Automatic (Push to main)**
```bash
git add .
git commit -m "Enable CI/CD"
git push origin main
```

**Option B: Manual Trigger**
1. Go to **Actions** tab
2. Select workflow (e.g., "Train Model")
3. Click **Run workflow**
4. Choose options and click **Run**

## 🎯 Common Use Cases

### Train a New Model

1. Go to **Actions** → **Train Model**
2. Click **Run workflow**
3. Select model type and options
4. Click **Run workflow**
5. Check results in artifacts

### Deploy to Production

**Automatic:**
- Push changes to `main` branch
- Deployment runs automatically

**Manual:**
1. Go to **Actions** → **Deploy to AWS**
2. Click **Run workflow**
3. Select environment (production/staging)
4. Click **Run workflow**

### Retrain and Auto-Deploy

1. Go to **Actions** → **Retrain and Deploy**
2. Click **Run workflow**
3. Set MSE threshold (default: 5.0)
4. Click **Run workflow**
5. Model deploys only if MSE < threshold

## 📊 Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. Select workflow
3. View run history and logs

### Check Deployment Status

1. Go to **Actions** → Recent runs
2. Click on run → **Summary**
3. View deployment details and API URL

### Download Artifacts

1. Go to completed workflow run
2. Scroll to **Artifacts** section
3. Download model files or metrics

## 🐛 Troubleshooting

### Workflow Fails - AWS Credentials

**Error:** "Unable to locate credentials"

**Solution:**
1. Verify AWS secrets are set correctly
2. Check secret names match exactly
3. Ensure AWS credentials are valid

### Workflow Fails - Model Training

**Error:** "No module named 'zenml'"

**Solution:**
- Check `requirements.txt` is up to date
- Verify Python version in workflow (3.12)

### Deployment Fails - Stack Already Exists

**Error:** "Stack already exists"

**Solution:**
- This is normal, deployment will update existing stack
- Check workflow logs for actual error

## 🔄 Workflow Dependencies

```
┌─────────────┐
│   CI Test   │ ← Runs on every push/PR
└─────────────┘

┌─────────────┐
│ Train Model │ ← Manual or scheduled
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│ Deploy to AWS   │ ← Automatic on main push
└─────────────────┘

┌──────────────────────┐
│ Retrain and Deploy   │ ← Manual or monthly
│  (Combined workflow) │
└──────────────────────┘
```

## 📈 Best Practices

1. **Always run CI before merging**
   - Create PR for code changes
   - Wait for CI to pass
   - Then merge to main

2. **Test deployments in staging first**
   - Use manual trigger with staging environment
   - Verify API works
   - Then deploy to production

3. **Monitor model performance**
   - Check training metrics regularly
   - Set appropriate MSE thresholds
   - Review deployment summaries

4. **Keep secrets secure**
   - Never commit secrets to code
   - Rotate AWS keys periodically
   - Use least-privilege IAM policies

## 🎓 Learn More

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [AWS SAM Docs](https://docs.aws.amazon.com/serverless-application-model/)
- [MLflow Docs](https://mlflow.org/docs/latest/index.html)
- [ZenML Docs](https://docs.zenml.io)
