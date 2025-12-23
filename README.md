# 🚀 Customer Satisfaction Prediction - End-to-End MLOps Project

A production-ready MLOps pipeline for predicting customer satisfaction scores using ZenML, MLflow, and AWS Lambda.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MLflow](https://img.shields.io/badge/MLflow-2.18.0-blue.svg)](https://mlflow.org/)
[![ZenML](https://img.shields.io/badge/ZenML-0.92.0-green.svg)](https://zenml.io/)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [AWS Deployment](#aws-deployment)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Results](#results)

## 🎯 Overview

This project implements a complete MLOps pipeline for predicting customer satisfaction based on order details. It demonstrates:

- **Automated ML Pipeline**: Data ingestion → Cleaning → Training → Evaluation → Deployment
- **Experiment Tracking**: MLflow for tracking experiments and model registry
- **Pipeline Orchestration**: ZenML for managing ML workflows
- **Serverless Deployment**: AWS Lambda for cost-effective, scalable inference
- **Continuous Deployment**: Automated model deployment based on performance metrics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     MLOps Pipeline Architecture                  │
└─────────────────────────────────────────────────────────────────┘

Data Ingestion → Data Cleaning → Model Training → Evaluation
                                        ↓
                                  MLflow Tracking
                                        ↓
                            Deployment Decision (MSE < 5.0)
                                        ↓
                              ┌─────────┴─────────┐
                              │                   │
                        Local Serving      AWS Lambda + API Gateway
                        (Development)         (Production)
                              │                   │
                         localhost:8000    Public HTTPS Endpoint
```

## ✨ Features

### ML Pipeline
- ✅ **Data Ingestion**: Automated data loading from multiple sources
- ✅ **Data Cleaning**: Handle missing values, outliers, feature engineering
- ✅ **Model Training**: Linear Regression with configurable models (LightGBM, XGBoost, Random Forest)
- ✅ **Evaluation**: MSE, RMSE, R2 metrics tracking
- ✅ **Deployment Trigger**: Automated deployment based on performance threshold

### MLOps Features
- ✅ **Experiment Tracking**: All experiments logged to MLflow
- ✅ **Model Registry**: Version control for models
- ✅ **Pipeline Orchestration**: ZenML manages workflow dependencies
- ✅ **Continuous Deployment**: Auto-deploy models meeting criteria
- ✅ **Model Serving**: REST API for predictions

### Production Features
- ✅ **Serverless**: AWS Lambda for scalable, cost-effective inference
- ✅ **API Gateway**: HTTPS endpoint with CORS support
- ✅ **Health Checks**: Monitoring endpoint for service health
- ✅ **Versioning**: Model version tracking in responses

## 🛠️ Tech Stack

**ML & MLOps:**
- Python 3.12
- Scikit-learn, LightGBM, XGBoost
- MLflow (Experiment Tracking & Model Registry)
- ZenML (Pipeline Orchestration)
- Pandas, NumPy

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
python run_pipeline.py

# 6. View MLflow UI
mlflow ui --backend-store-uri "file:$HOME/Library/Application Support/zenml/local_stores/*/mlruns"
# Open http://localhost:5000

# 7. Run deployment pipeline
python run_deployment.py --config deploy_and_predict
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
# 1. Deploy infrastructure and Lambda function
./deploy_aws.sh

# 2. Upload trained model to S3
./upload_model.sh

# 3. Test the API
./test_api.sh
```

Your API will be available at:
```
https://<api-id>.execute-api.<region>.amazonaws.com/prod/predict
```

## 📁 Project Structure

```
fcc_mlops_project/
├── pipelines/
│   ├── training_pipeline.py          # Training pipeline definition
│   └── deployment_pipeline.py        # Deployment pipeline definition
├── steps/
│   ├── ingest_data.py                # Data ingestion step
│   ├── clean_data.py                 # Data cleaning step
│   ├── model_train.py                # Model training step
│   ├── evaluation.py                 # Model evaluation step
│   └── config.py                     # Configuration classes
├── src/
│   ├── data_cleaning.py              # Data cleaning logic
│   ├── evaluation.py                 # Evaluation metrics
│   └── model_dev.py                  # Model development code
├── model/
│   └── model_dev.py                  # Model implementations
├── lambda_function.py                # AWS Lambda handler
├── template.yaml                     # AWS SAM template
├── deploy_aws.sh                     # AWS deployment script
├── upload_model.sh                   # Model upload script
├── test_api.sh                       # API testing script
├── run_pipeline.py                   # Training pipeline runner
├── run_deployment.py                 # Deployment pipeline runner
└── requirements.txt                  # Python dependencies
```

## 📡 API Documentation

### Prediction Endpoint

**URL:** `POST /predict`

**Request Body:**
```json
{
  "payment_sequential": 1,
  "payment_installments": 3,
  "payment_value": 142.90,
  "price": 129.99,
  "freight_value": 12.91,
  "product_name_lenght": 58,
  "product_description_lenght": 598,
  "product_photos_qty": 4,
  "product_weight_g": 700,
  "product_length_cm": 18,
  "product_height_cm": 9,
  "product_width_cm": 15
}
```

**Response:**
```json
{
  "prediction": 3.45,
  "customer_satisfaction_score": 3.45,
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
  "service": "customer-satisfaction-predictor",
  "version": "v1.0"
}
```

### Example Usage

**cURL:**
```bash
curl -X POST https://your-api-url/prod/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "payment_sequential": 1,
    "payment_installments": 3,
    "payment_value": 100.0,
    "price": 80.0,
    "freight_value": 10.0,
    "product_name_lenght": 50,
    "product_description_lenght": 200,
    "product_photos_qty": 3,
    "product_weight_g": 1000,
    "product_length_cm": 20,
    "product_height_cm": 10,
    "product_width_cm": 15
  }'
```

**Python:**
```python
import requests

url = "https://your-api-url/prod/predict"
data = {
    "payment_sequential": 1,
    "payment_installments": 3,
    "payment_value": 142.90,
    "price": 129.99,
    "freight_value": 12.91,
    "product_name_lenght": 58,
    "product_description_lenght": 598,
    "product_photos_qty": 4,
    "product_weight_g": 700,
    "product_length_cm": 18,
    "product_height_cm": 9,
    "product_width_cm": 15
}

response = requests.post(url, json=data)
print(response.json())
```

## 📊 Results

### Model Performance

| Model | MSE | RMSE | R2 Score |
|-------|-----|------|----------|
| LinearRegression | 1.864 | 1.365 | 0.018 |
| LightGBM | 1.804 | 1.343 | - |
| XGBoost | 1.781 | 1.335 | - |

### Feature Importance

Key features affecting customer satisfaction:
1. Payment Value
2. Price
3. Freight Value
4. Product Weight
5. Product Dimensions

## 🔧 Configuration

### Model Configuration

Edit `steps/config.py`:
```python
class ModelNameConfig(BaseModel):
    model_name: str = "LinearRegressionModel"  # or "lightgbm", "xgboost", "randomforest"
    fine_tuning: bool = False
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
python run_deployment.py --config deploy
```

## 📚 Learn More

- [ZenML Documentation](https://docs.zenml.io)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Sai Sujan**

Feel free to reach out for questions or collaboration!

---

**⭐ If you found this project helpful, please give it a star!**
