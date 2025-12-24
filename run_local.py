from pipelines.training_pipeline import train_pipeline
from steps.config import ModelNameConfig, DataConfig
from zenml.client import Client

if __name__ == "__main__":
    """
    LOCAL Training - Saves model locally only
    Run: python run_local.py
    """

    print(Client().active_stack.experiment_tracker.get_tracking_uri())

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
