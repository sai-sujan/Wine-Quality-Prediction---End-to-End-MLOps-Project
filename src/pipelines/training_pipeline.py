from zenml import pipeline
from src.steps.ingest_data import ingest_df
from src.steps.clean_data import clean_df
from src.steps.model_train import train_model
from src.steps.evaluation import evaluate_model
from src.steps.save_model import save_model
import logging
from src.steps.config import ModelNameConfig, DataConfig

@pipeline(enable_cache=True)
def train_pipeline(data_config: DataConfig, model_config: ModelNameConfig):
    """
    Wine Quality Prediction Training Pipeline

    Args:
        data_config: Configuration for data ingestion (URL, wine type)
        model_config: Configuration for model training (model name, hyperparameter tuning)
    """
    df = ingest_df(config=data_config)
    X_train, X_test, y_train, y_test = clean_df(df)
    model = train_model(X_train, X_test, y_train, y_test, config=model_config)
    r2_score, rmse = evaluate_model(model, X_test, y_test)
    save_model(model)

