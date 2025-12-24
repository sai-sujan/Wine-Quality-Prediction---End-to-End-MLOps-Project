from pydantic import BaseModel

class DataConfig(BaseModel):
    """Data ingestion config"""
    data_url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    wine_type: str = "red"  # Options: "red", "white", "combined"

class ModelNameConfig(BaseModel):
    """Model config"""
    model_name: str = "LinearRegressionModel"
    fine_tuning: bool = False
    use_cached_params: bool = True  # Use previously optimized hyperparameters if available
    save_to_s3: bool = False  # Save model/params to S3
    load_from_s3: bool = False  # Load model from S3
