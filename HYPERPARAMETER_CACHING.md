# 💾 Hyperparameter Caching Feature

## Overview

Your MLOps pipeline now **saves and reuses** the best hyperparameters found during optimization! This means:

✅ **First run**: Runs 100 trials (~2-5 minutes) to find optimal parameters
✅ **Subsequent runs**: Uses cached parameters instantly (saves ~2-5 minutes each time!)

## How It Works

### 1. First Training Run

When you run the pipeline for the first time:

```bash
python run_pipeline.py
```

Output:
```
🔬 Starting hyperparameter optimization for randomforest (100 trials)...
[I] Trial 1 finished with value: 0.5234
[I] Trial 2 finished with value: 0.5891
...
[I] Trial 100 finished with value: 0.6287
✨ Optimization complete!
   Best R² Score: 0.6287
   Best Parameters: {'n_estimators': 120, 'max_depth': 12, 'min_samples_split': 3}
💾 Saved best hyperparameters for randomforest
```

The best parameters are saved to [best_params.json](best_params.json)

### 2. Subsequent Runs

Next time you run the pipeline:

```bash
python run_pipeline.py
```

Output:
```
✅ Loaded saved hyperparameters for randomforest:
   {'n_estimators': 120, 'max_depth': 12, 'min_samples_split': 3}
🚀 Using cached hyperparameters for randomforest (skipping 100 trials)
   Set use_cached=False to run optimization again
```

**Training completes in seconds instead of minutes!**

## Configuration

### Use Cached Parameters (Default)

```python
# In run_pipeline.py
model_config = ModelNameConfig(
    model_name="randomforest",
    fine_tuning=True,
    use_cached_params=True  # ← Uses saved parameters
)
```

### Force Re-optimization

To find new hyperparameters (e.g., if you changed the dataset):

```python
# In run_pipeline.py
model_config = ModelNameConfig(
    model_name="randomforest",
    fine_tuning=True,
    use_cached_params=False  # ← Runs 100 trials again
)
```

## Stored Parameters File

Location: [best_params.json](best_params.json)

Example content:
```json
{
  "randomforest": {
    "n_estimators": 120,
    "max_depth": 12,
    "min_samples_split": 3
  },
  "lightgbm": {
    "n_estimators": 150,
    "max_depth": 15,
    "learning_rate": 0.05
  },
  "xgboost": {
    "n_estimators": 100,
    "max_depth": 10,
    "learning_rate": 0.01
  },
  "LinearRegressionModel": {},
  "last_updated": "2025-12-23T17:30:00"
}
```

## When Parameters Are Saved

Parameters are automatically saved after successful optimization for:
- ✅ RandomForest
- ✅ LightGBM
- ✅ XGBoost
- ❌ LinearRegression (no hyperparameters to tune)

## Benefits

| Aspect | First Run | Cached Runs |
|--------|-----------|-------------|
| **Optimization Time** | ~2-5 minutes | ~0 seconds |
| **Total Pipeline Time** | ~3-6 minutes | ~1 minute |
| **Trials Run** | 100 trials | 0 trials |
| **Model Quality** | Optimized | Same quality |

## When to Re-optimize

Run with `use_cached_params=False` when:

1. **Dataset changed** - New wine type (red → white → combined)
2. **More data** - Dataset size significantly increased
3. **Better results** - Want to try more trials (change `n_trials=200`)
4. **Different features** - Feature engineering changes

## Example Workflow

```bash
# First time: Train with optimization
python run_pipeline.py  # Takes ~3-5 minutes, finds best params

# Subsequent times: Fast training with same params
python run_pipeline.py  # Takes ~1 minute, uses cached params
python run_pipeline.py  # Takes ~1 minute, uses cached params

# Changed to white wine? Re-optimize
# Edit run_pipeline.py: wine_type="white", use_cached_params=False
python run_pipeline.py  # Takes ~3-5 minutes, finds new best params

# Continue with white wine using cached params
# Edit run_pipeline.py: use_cached_params=True
python run_pipeline.py  # Takes ~1 minute, uses cached params
```

## Implementation Details

The caching is implemented in [src/model_dev.py](src/model_dev.py):

- `_load_best_params()`: Loads saved parameters for the current model
- `_save_best_params()`: Saves best parameters after optimization
- `optimize(use_cached=True)`: Main method with caching logic

## Clear Cache

To start fresh:

```bash
# Delete the cached parameters file
rm best_params.json

# Or edit it manually to remove specific model params
```

---

**💡 Pro Tip**: Keep `use_cached_params=True` for normal development. Only set to `False` when you need to re-optimize due to significant changes!
