from src.pipelines.training_pipeline import train_pipeline
from src.steps.config import ModelNameConfig, DataConfig
from zenml.client import Client

if __name__ == "__main__":
    """
    LOCAL Training - Saves model locally only
    Run: python run_local.py
    """

    # Print tracking URI if experiment tracker is configured
    experiment_tracker = Client().active_stack.experiment_tracker
    if experiment_tracker:
        print(f"MLflow tracking URI: {experiment_tracker.get_tracking_uri()}")
    else:
        print("No experiment tracker configured - using default MLflow settings")

    data_config = DataConfig(
        data_url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        wine_type="red"
    )

    model_config = ModelNameConfig(
        model_name="randomforest",
        fine_tuning=True,
        use_cached_params=True,
        save_to_s3=False,  # Local only
        load_from_s3=False
    )

    train_pipeline(data_config=data_config, model_config=model_config)
