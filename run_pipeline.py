from pipelines.training_pipeline import train_pipeline
from steps.config import ModelNameConfig, DataConfig

from zenml.client import Client

if __name__ == "__main__":
    """
    Wine Quality Prediction Pipeline

    This pipeline predicts wine quality scores (0-10) based on physicochemical properties.

    Configuration options:
    - wine_type: "red", "white", or "combined"
    - model_name: "LinearRegressionModel", "lightgbm", "xgboost", "randomforest"
    - fine_tuning: Enable hyperparameter optimization with Optuna
    """

    # Print MLflow tracking URI
    print(Client().active_stack.experiment_tracker.get_tracking_uri())

    # Configure data ingestion
    data_config = DataConfig(
        data_url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        wine_type="red"  # Options: "red", "white", "combined"
    )

    # Configure model training
    model_config = ModelNameConfig(
        model_name="randomforest",  # Options: "LinearRegressionModel", "lightgbm", "xgboost", "randomforest"
        fine_tuning=True,  # Enable hyperparameter tuning
        use_cached_params=True  # Use saved hyperparameters if available (set False to re-optimize)
    )

    # Run the training pipeline
    train_pipeline(data_config=data_config, model_config=model_config)

# MLflow UI command:
# mlflow ui --backend-store-uri "file:/Users/saisujan/Library/Application Support/zenml/local_stores/b368042e-441e-457a-92a6-cd3abc06cd3a/mlruns"    