import os
from pipelines.training_pipeline import train_pipeline
from steps.config import ModelNameConfig, DataConfig
from zenml.client import Client

if __name__ == "__main__":
    """
    AWS Training - Saves model to S3
    Run: python run_aws.py
    """

    # Enable S3 upload via environment variable
    os.environ['SAVE_TO_S3'] = 'true'
    os.environ['AWS_BUCKET_NAME'] = 'wine-quality-mlops-sujan'
    os.environ['AWS_REGION'] = 'us-east-2'

    print(Client().active_stack.experiment_tracker.get_tracking_uri())

    data_config = DataConfig(
        data_url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        wine_type="red"
    )

    model_config = ModelNameConfig(
        model_name="randomforest",
        fine_tuning=True,
        use_cached_params=True,
        save_to_s3=True,  # Upload to S3
        load_from_s3=False
    )

    train_pipeline(data_config=data_config, model_config=model_config)
