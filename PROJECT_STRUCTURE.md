# Project Structure

## 📁 Clean Project Layout

```
fcc_mlops_project/
├── .github/workflows/          # CI/CD GitHub Actions
│   ├── ci.yml                 # Continuous Integration
│   ├── train-model.yml        # Model Training
│   ├── deploy-aws.yml         # AWS Deployment
│   ├── retrain-and-deploy.yml # Smart Retrain & Deploy
│   └── README.md              # Workflows documentation
│
├── pipelines/                  # ZenML Pipelines
│   ├── __init__.py
│   ├── training_pipeline.py   # Training pipeline
│   ├── deployment_pipeline.py # Deployment pipeline
│   └── utils.py               # Pipeline utilities
│
├── steps/                      # ZenML Pipeline Steps
│   ├── __init__.py
│   ├── ingest_data.py         # Data ingestion
│   ├── clean_data.py          # Data cleaning
│   ├── model_train.py         # Model training
│   ├── evaluation.py          # Model evaluation
│   └── config.py              # Step configurations
│
├── src/                        # Core ML Logic
│   ├── __init__.py
│   ├── data_cleaning.py       # Data cleaning implementations
│   ├── evaluation.py          # Evaluation metrics
│   └── model_dev.py           # Model implementations
│
├── model/                      # Model code (legacy - same as src)
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── evaluation.py
│   └── model_dev.py
│
├── lambda_function.py          # AWS Lambda handler
├── template.yaml               # AWS SAM template
├── lambda_requirements.txt     # Lambda dependencies
│
├── deploy_aws.sh               # AWS deployment script
├── upload_model.sh             # Model upload script
├── test_api.sh                 # API testing script
│
├── run_pipeline.py             # Run training pipeline
├── run_deployment.py           # Run deployment pipeline
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── .yamllint                   # YAML linting config
│
├── README.md                   # Main project documentation
├── AWS_DEPLOYMENT_GUIDE.md     # AWS deployment guide
├── CICD_SETUP.md               # CI/CD setup guide
└── PROJECT_STRUCTURE.md        # This file
```


## 📝 Key Files

### Documentation
- **README.md** - Main project overview and quick start
- **AWS_DEPLOYMENT_GUIDE.md** - Complete AWS deployment guide
- **CICD_SETUP.md** - CI/CD pipeline setup instructions
- **.github/workflows/README.md** - Workflows documentation

### AWS Deployment
- **template.yaml** - CloudFormation/SAM infrastructure
- **lambda_function.py** - Lambda function for predictions
- **deploy_aws.sh** - One-click AWS deployment
- **upload_model.sh** - Upload model to S3
- **test_api.sh** - Test deployed API

### ML Pipeline
- **pipelines/training_pipeline.py** - Training workflow
- **pipelines/deployment_pipeline.py** - Deployment workflow
- **run_pipeline.py** - Execute training
- **run_deployment.py** - Execute deployment

### CI/CD
- **.github/workflows/ci.yml** - Tests on every push
- **.github/workflows/train-model.yml** - Scheduled training
- **.github/workflows/deploy-aws.yml** - Auto-deploy
- **.github/workflows/retrain-and-deploy.yml** - Smart deployment

## 🎯 File Purpose

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_pipeline.py` | Train model locally | Development/testing |
| `run_deployment.py` | Deploy model locally | Testing deployment |
| `deploy_aws.sh` | Deploy to AWS | Production deployment |
| `.github/workflows/*` | CI/CD automation | Automatic on git push |

## 🔧 Configuration Files

- **requirements.txt** - Python packages for local development
- **lambda_requirements.txt** - Python packages for Lambda (minimal)
- **.gitignore** - Files to exclude from git
- **.yamllint** - YAML linting rules
- **.vscode/settings.json** - VSCode IDE configuration

## 📦 Artifacts (Not in Git)

These are generated and excluded from version control:

```
.zenml/                # ZenML metadata (local)
mlruns/                # MLflow experiments (local)
zenml_env/             # Python virtual environment
__pycache__/           # Python cache
*.pyc                  # Compiled Python
.aws-sam/              # SAM build artifacts
packaged.yaml          # SAM package output
```

## 🚀 Quick Start

1. **Local Development:**
   ```bash
   python run_pipeline.py
   ```

2. **Local Deployment:**
   ```bash
   python run_deployment.py --config deploy
   ```

3. **AWS Deployment:**
   ```bash
   ./deploy_aws.sh
   ```

4. **CI/CD (Automatic):**
   ```bash
   git push origin main  # Auto-deploys via GitHub Actions
   ```

## 📊 Project Stats

- **Total Python files:** ~20
- **Total lines of code:** ~3000
- **Workflows:** 4 automated pipelines
- **Documentation files:** 4
- **Shell scripts:** 3
s
## 🔄 Data Flow

```
Data → Ingest → Clean → Train → Evaluate → Deploy → API
         ↓        ↓       ↓        ↓         ↓      ↓
      ZenML   ZenML   MLflow   MLflow    Lambda  Users
```

## ✅ Clean Structure Benefits

1. **No Docker complexity** - Uses AWS Lambda (serverless)
2. **No Streamlit** - Professional API endpoint instead
3. **Minimal files** - Only essential components
4. **Clear separation** - Pipelines, steps, source code
5. **CI/CD ready** - GitHub Actions workflows
6. **Production ready** - AWS infrastructure as code
