# 🍷 Wine Quality Prediction - End-to-End MLOps Project

A production-ready MLOps pipeline for predicting wine quality scores using ZenML, MLflow, and AWS Lambda.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MLflow](https://img.shields.io/badge/MLflow-2.18.0-blue.svg)](https://mlflow.org/)
[![ZenML](https://img.shields.io/badge/ZenML-0.92.0-green.svg)](https://zenml.io/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [AWS Deployment](#aws-deployment)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Results](#results)

## 🎯 Overview

This project implements a complete MLOps pipeline for predicting wine quality scores (0-10) based on physicochemical properties. It demonstrates:

- **Automated ML Pipeline**: Data ingestion → Cleaning → Training → Evaluation → Deployment
- **URL-Based Data Ingestion**: Fetches data directly from UCI repository
- **Experiment Tracking**: MLflow for tracking experiments and model registry
- **Pipeline Orchestration**: ZenML for managing ML workflows
- **Serverless Deployment**: AWS Lambda for cost-effective, scalable inference
- **Continuous Deployment**: Automated model deployment based on performance metrics

## 📊 Dataset

**Source**: [UCI Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)

### Features (11 physicochemical properties):
- **Fixed Acidity**: Tartaric acid concentration (g/dm³)
- **Volatile Acidity**: Acetic acid concentration (g/dm³)
- **Citric Acid**: Adds freshness and flavor (g/dm³)
- **Residual Sugar**: Sugar remaining after fermentation (g/dm³)
- **Chlorides**: Salt content (g/dm³)
- **Free Sulfur Dioxide**: Free form of SO₂ (mg/dm³)
- **Total Sulfur Dioxide**: Total SO₂ content (mg/dm³)
- **Density**: Wine density (g/cm³)
- **pH**: Acidity level (0-14 scale)
- **Sulphates**: Potassium sulphate - antimicrobial & antioxidant (g/dm³)
- **Alcohol**: Alcohol content (% by volume)

### Target Variable:
- **Quality**: Score between 0-10 (based on sensory data)

### Dataset Variants:
- **Red Wine**: 1,599 samples
- **White Wine**: 4,898 samples
- **Combined**: 6,497 samples (both types)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MLOps Pipeline Architecture                  │
└─────────────────────────────────────────────────────────────────┘

URL Data Ingestion → Data Cleaning → Model Training → Evaluation
   (UCI Dataset)                            ↓
                                      MLflow Tracking
                                            ↓
                                Deployment Decision (MSE < 5.0)
                                            ↓
                              ┌─────────────┴─────────────┐
                              │                           │
                        Local Serving            AWS Lambda + API Gateway
                        (Development)                 (Production)
                              │                           │
                         localhost:8000          Public HTTPS Endpoint
```

## ✨ Features

### ML Pipeline
- ✅ **URL-Based Data Ingestion**: Fetch data directly from UCI repository
- ✅ **Multi-Dataset Support**: Red, White, or Combined wine datasets
- ✅ **Data Cleaning**: Handle missing values, duplicates, encoding
- ✅ **Model Training**: RandomForest with hyperparameter tuning (Optuna)
- ✅ **Multiple Models**: LinearRegression, LightGBM, XGBoost, RandomForest
- ✅ **Evaluation**: MSE, RMSE, R2 metrics tracking
- ✅ **Stratified Splitting**: Ensures balanced quality distribution

### MLOps Features
- ✅ **Experiment Tracking**: All experiments logged to MLflow
- ✅ **Model Registry**: Version control for models
- ✅ **Pipeline Orchestration**: ZenML manages workflow dependencies
- ✅ **Hyperparameter Tuning**: Optuna integration for model optimization
- ✅ **Continuous Deployment**: Auto-deploy models meeting criteria
- ✅ **Model Serving**: REST API for predictions

### Production Features
- ✅ **Serverless**: AWS Lambda for scalable, cost-effective inference
- ✅ **API Gateway**: HTTPS endpoint with CORS support
- ✅ **Health Checks**: Monitoring endpoint for service health
- ✅ **Versioning**: Model version tracking in responses
- ✅ **Interactive Dashboard**: Streamlit UI for wine quality predictions

## 🛠️ Tech Stack

**ML & MLOps:**
- Python 3.12
- Scikit-learn, LightGBM, XGBoost
- Optuna (Hyperparameter Optimization)
- MLflow (Experiment Tracking & Model Registry)
- ZenML (Pipeline Orchestration)
- Pandas, NumPy

**API & Development:**
- FastAPI (Local Development & Testing)
- Uvicorn (ASGI Server)
- Pydantic (Data Validation)
- Auto-generated API Documentation

**UI & Visualization:**
- Streamlit (Production Dashboard)
- Plotly (Interactive Charts & Gauges)
- Real-time Monitoring & Analytics

**Deployment:**
- AWS Lambda (Serverless Compute)
- AWS API Gateway (REST API)
- AWS S3 (Model Storage)
- AWS SAM (Infrastructure as Code)

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python 3.12
# macOS
brew install python@3.12

# Create virtual environment
python3.12 -m venv zenml_env
source zenml_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Local Development

```bash
# 1. Initialize ZenML
zenml init

# 2. Install MLflow integration
zenml integration install mlflow -y

# 3. Register MLflow tracker
zenml experiment-tracker register mlflow_tracker --flavor=mlflow

# 4. Create and set stack
zenml stack register mlflow_stack \
    -o default \
    -a default \
    -e mlflow_tracker

zenml stack set mlflow_stack

# 5. Run the training pipeline
python scripts/run_local.py

# 6. Start FastAPI server (for local testing)
python src/api/main.py
# Open http://localhost:8000/docs

# 7. View MLflow UI
mlflow ui --backend-store-uri "file:$HOME/Library/Application Support/zenml/local_stores/*/mlruns"
# Open http://localhost:5000

# 8. Start Streamlit Dashboard (Production UI)
streamlit run src/dashboard/streamlit_app.py
# Open http://localhost:8501
```

## ☁️ AWS Deployment

### Prerequisites

1. **AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **AWS CLI**: Install from [aws.amazon.com/cli](https://aws.amazon.com/cli/)
3. **AWS SAM CLI**: Install from [AWS SAM docs](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

```bash
# macOS
brew install aws-sam-cli
```

### Configure AWS

```bash
# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., us-east-1)
```

### Deploy to AWS

```bash
# Complete AWS deployment (setup S3, train model, deploy Lambda)
./deployment/aws/scripts/deploy_all.sh

# Or run individual steps:
# 1. Setup S3 bucket
./deployment/aws/scripts/setup_s3.sh

# 2. Train and upload model to S3
./deployment/aws/scripts/train_aws.sh

# 3. Deploy Lambda function with Layer
./deployment/aws/scripts/deploy_lambda_with_layer.sh
```

Your API will be available at:
```
https://<api-id>.execute-api.<region>.amazonaws.com/prod/predict
```

## 📁 Project Structure

```
fcc_mlops_project/
├── pipelines/
���   ├── training_pipeline.py          # Training pipeline definition
│   └── deployment_pipeline.py        # Deployment pipeline definition
├── steps/
│   ├── ingest_data.py                # URL-based data ingestion
│   ├── clean_data.py                 # Data cleaning step
│   ├── model_train.py                # Model training step
│   ├── evaluation.py                 # Model evaluation step
│   └── config.py                     # Configuration classes
├── src/
│   ├── data_cleaning.py              # Data cleaning logic
│   ├── evaluation.py                 # Evaluation metrics
│   └── model_dev.py                  # Model development code
├── api.py                            # FastAPI application (local dev)
├── lambda_function.py                # AWS Lambda handler (production)
├── streamlit_dashboard.py            # Streamlit production UI
├── template.yaml                     # AWS SAM template
├── deploy_aws.sh                     # AWS deployment script
├── upload_model.sh                   # Model upload script
├── test_api.sh                       # API testing script
├── run_api.sh                        # Start FastAPI server
├── run_dashboard.sh                  # Start Streamlit dashboard
├── run_pipeline.py                   # Training pipeline runner
├── run_deployment.py                 # Deployment pipeline runner
└── requirements.txt                  # Python dependencies
```

## 🎨 Streamlit Wine Quality Dashboard

A beautiful, interactive web interface for making wine quality predictions!

### Features

- **🍷 Wine Type Selection** - Choose between Red or White wine
- **🧪 Chemical Properties Input** - 11 physicochemical feature inputs with helpful tooltips
- **🔮 Interactive Predictions** - Beautiful gauge visualization with quality ratings
- **📊 Real-time API Status** - Automatic check if prediction service is running
- **💻 Professional UI** - Clean design with wine-themed colors

### Quality Ratings
- **Excellent** (7-10): Premium quality wine
- **Good** (6-7): Good quality wine
- **Average** (5-6): Average quality wine
- **Poor** (0-5): Needs improvement

### Quick Start

```bash
# Terminal 1: Start FastAPI (for local predictions)
python src/api/main.py

# Terminal 2: Start Streamlit Dashboard
streamlit run src/dashboard/streamlit_app.py

# Open in browser
http://localhost:8501
```

## 📡 API Documentation

### Prediction Endpoint

**URL:** `POST /predict`

**Request Body:**
```json
{
  "fixed_acidity": 7.4,
  "volatile_acidity": 0.70,
  "citric_acid": 0.0,
  "residual_sugar": 1.9,
  "chlorides": 0.076,
  "free_sulfur_dioxide": 11.0,
  "total_sulfur_dioxide": 34.0,
  "density": 0.9978,
  "pH": 3.51,
  "sulphates": 0.56,
  "alcohol": 9.4,
  "wine_type_encoded": 0
}
```

**Response:**
```json
{
  "prediction": 5.8,
  "wine_quality_score": 5.8,
  "quality_rating": "Average",
  "model_version": "v1.0",
  "message": "Prediction successful"
}
```

### Health Check Endpoint

**URL:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "wine-quality-predictor",
  "version": "v1.0",
  "model_loaded": true
}
```

### Model Info Endpoint

**URL:** `GET /model/info`

**Response:**
```json
{
  "model_type": "RandomForestRegressor",
  "problem_type": "Wine Quality Prediction (Regression)",
  "target": "quality (0-10 score)",
  "features": [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "residual sugar",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "wine_type_encoded"
  ],
  "version": "v1.0"
}
```

### Example Usage

**cURL:**
```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.70,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
    "wine_type_encoded": 0
  }'
```

**Python:**
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "fixed_acidity": 7.4,
    "volatile_acidity": 0.70,
    "citric_acid": 0.0,
    "residual_sugar": 1.9,
    "chlorides": 0.076,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 34.0,
    "density": 0.9978,
    "pH": 3.51,
    "sulphates": 0.56,
    "alcohol": 9.4,
    "wine_type_encoded": 0
}

response = requests.post(url, json=data)
result = response.json()
print(f"Wine Quality: {result['wine_quality_score']:.2f}/10 - {result['quality_rating']}")
```

## 📊 Results

### Expected Model Performance

RandomForest with hyperparameter tuning typically achieves:

| Metric | Expected Range |
|--------|----------------|
| **R² Score** | 0.55 - 0.65 |
| **RMSE** | 0.55 - 0.65 |
| **MSE** | 0.30 - 0.42 |

These results are significantly better than the previous customer satisfaction model due to:
- Better dataset quality (UCI Wine Quality is clean with no missing values)
- More predictive features (physicochemical properties directly impact wine quality)
- RandomForest model with hyperparameter tuning
- Stratified train-test splitting

### Feature Importance

Key features affecting wine quality:
1. **Alcohol**: Higher alcohol content often correlates with better quality
2. **Volatile Acidity**: Lower acidity indicates better quality
3. **Sulphates**: Antimicrobial properties affect wine preservation
4. **Citric Acid**: Adds freshness to the wine
5. **Total Sulfur Dioxide**: Preservative levels

## 🔧 Configuration

### Data Configuration

Edit `steps/config.py`:
```python
class DataConfig(BaseModel):
    data_url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    wine_type: str = "red"  # Options: "red", "white", "combined"
```

### Model Configuration

Edit `steps/config.py`:
```python
class ModelNameConfig(BaseModel):
    model_name: str = "randomforest"  # or "LinearRegressionModel", "lightgbm", "xgboost"
    fine_tuning: bool = True  # Enable hyperparameter tuning with Optuna
```

Edit `run_pipeline.py` to change configuration:
```python
# Configure data ingestion
data_config = DataConfig(
    data_url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
    wine_type="red"  # Try "white" or "combined"
)

# Configure model training
model_config = ModelNameConfig(
    model_name="randomforest",  # Options: "LinearRegressionModel", "lightgbm", "xgboost", "randomforest"
    fine_tuning=True
)
```

### Deployment Configuration

Edit `pipelines/deployment_pipeline.py`:
```python
class DeploymentTriggerConfig(BaseModel):
    max_mse: float = 5.0  # Deploy if MSE < 5.0
```

## 🐛 Troubleshooting

**MLflow UI not starting:**
```bash
# Find and use the correct MLflow tracking URI
find ~/Library -name "mlruns" 2>/dev/null
mlflow ui --backend-store-uri "file:/path/to/mlruns"
```

**Data ingestion fails:**
```bash
# Check internet connection and URL accessibility
curl -I https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
```

**AWS deployment fails:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify SAM CLI installation
sam --version
```

**Model not found error:**
```bash
# Train a model first
python scripts/run_local.py
```

## 📚 Learn More

- [UCI Wine Quality Dataset](https://archive.ics.uci.edu/ml/datasets/wine+quality)
- [ZenML Documentation](https://docs.zenml.io)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Sai Sujan**

Feel free to reach out for questions or collaboration!

---

**⭐ If you found this project helpful, please give it a star!**
