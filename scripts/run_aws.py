import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipelines.training_pipeline import train_pipeline
from src.steps.config import ModelNameConfig, DataConfig
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
        save_to_s3=True,  # Upload to S3
        load_from_s3=False
    )

    train_pipeline(data_config=data_config, model_config=model_config)
