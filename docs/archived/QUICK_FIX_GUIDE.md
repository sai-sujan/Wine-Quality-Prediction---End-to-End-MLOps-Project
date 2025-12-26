# 🔧 Quick Fix Guide - Prediction Error

## ❌ The Problem

Your API is showing errors because:
1. The **old model** (in `models/model.pkl`) was trained on the **customer satisfaction dataset**
2. Your **new API** expects **wine quality features**
3. This is a **feature mismatch** - the model expects different columns than what the API is sending

## ✅ The Solution

You need to **train a new model** with the wine quality dataset. Follow these steps:

### Step 1: Activate Virtual Environment

```bash
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project
source zenml_env/bin/activate
```

### Step 2: Test Data Ingestion (Optional)

```bash
python test_data_ingestion.py
```

This should show you that wine data is being fetched correctly.

### Step 3: Train New Model

```bash
python run_pipeline.py
```

**Note**: The model will use RandomForest with hyperparameter tuning (configured in run_pipeline.py)

This will:
- Fetch wine quality data from UCI repository
- Preprocess it
- Train RandomForest model with hyperparameter tuning
- Save the new model
- Log metrics to MLflow

**Expected Output:**
```
Fetching red wine data from URL: https://...
Successfully loaded 1599 records with 13 columns
Training RandomForest with hyperparameter tuning...
R² Score: 0.55-0.65
RMSE: 0.55-0.65
```

### Step 4: Start API Server

After training completes:

```bash
# In terminal 1
./run_api.sh
```

Visit: http://localhost:8000/docs

### Step 5: Start Dashboard

```bash
# In terminal 2
./run_dashboard.sh
```

Visit: http://localhost:8501

## 🐛 Troubleshooting

### Error: "Virtual environment not activated"
```bash
source zenml_env/bin/activate
```

### Error: "ZenML not initialized"
```bash
zenml init
zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml stack register mlflow_stack -o default -a default -e mlflow_tracker
zenml stack set mlflow_stack
```

### Error: "Model not found"
- Make sure `python run_pipeline.py` completed successfully
- Check that `models/model.pkl` was updated (check timestamp)

### Error: "Feature mismatch"
- This means you're still using the old model
- Delete the old model: `rm models/model.pkl`
- Train new model: `python run_pipeline.py`

## 📊 Verify Model Features

After training, verify the model has correct features:

```bash
python -c "
import joblib
model = joblib.load('models/model.pkl')
if hasattr(model, 'feature_names_in_'):
    print('Expected features:', list(model.feature_names_in_))
"
```

Should show wine quality features like:
- fixed acidity
- volatile acidity
- citric acid
- etc.

## ✨ Once Training is Complete

Your API will work with requests like:

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

And return:

```json
{
  "prediction": 5.8,
  "wine_quality_score": 5.8,
  "quality_rating": "Average",
  "model_version": "v1.0",
  "message": "Prediction successful"
}
```

---

**Summary**: The old model doesn't match the new API. Just run `python run_pipeline.py` to train a new model with wine quality data! 🍷
