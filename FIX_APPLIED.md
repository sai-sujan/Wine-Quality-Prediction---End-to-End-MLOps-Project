# ✅ Fix Applied - Model Name Corrected

## The Error You Had

```
ValueError: Model name not supported
```

## The Problem

In [run_pipeline.py:29](run_pipeline.py#L29), the model name was set to:
```python
model_name="RandomForestModel"  # ❌ WRONG
```

But the code in [steps/model_train.py:45](steps/model_train.py#L45) expects:
```python
elif config.model_name == "randomforest":  # ✅ Lowercase
```

## The Fix

I changed [run_pipeline.py:29](run_pipeline.py#L29) to:
```python
model_name="randomforest"  # ✅ CORRECT
```

## Valid Model Names

According to [steps/model_train.py](steps/model_train.py#L42-L53), the valid model names are:

| Model Name (for config) | Model Class | Auto-logging |
|------------------------|-------------|--------------|
| `"lightgbm"` | LightGBMModel | mlflow.lightgbm |
| `"randomforest"` | RandomForestModel | mlflow.sklearn |
| `"xgboost"` | XGBoostModel | mlflow.xgboost |
| `"LinearRegressionModel"` | LinearRegressionModel | mlflow.sklearn |

**Note**: Only `LinearRegressionModel` has capital letters - all others are lowercase!

## Now Run This

```bash
# Make sure you're in the right directory
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project

# Activate virtual environment (if not already)
source zenml_env/bin/activate

# Run the training pipeline (should work now!)
python run_pipeline.py
```

This will:
1. ✅ Fetch wine quality data from UCI (1,599 red wine samples)
2. ✅ Preprocess the data (handle missing values, encode wine type)
3. ✅ Train RandomForest model with Optuna hyperparameter tuning
4. ✅ Evaluate and log to MLflow
5. ✅ Save model to `models/model.pkl`

**Expected runtime**: ~2-5 minutes (hyperparameter tuning takes time)

## After Training Completes

1. **Start API**:
   ```bash
   ./run_api.sh
   ```
   Visit: http://localhost:8000/docs

2. **Start Dashboard**:
   ```bash
   ./run_dashboard.sh
   ```
   Visit: http://localhost:8501

3. **Test prediction** - Use the example from API docs:
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

Predictions will now work! 🎉
