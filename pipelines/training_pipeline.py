from zenml import pipeline
from steps.ingest_data import ingest_df
from steps.clean_data import clean_df
from steps.model_train import train_model
from steps.evaluation import evaluate_model
import logging
from steps.config import ModelNameConfig
@pipeline(enable_cache = True)
def train_pipeline(config: ModelNameConfig):
    df = ingest_df()
    X_train,X_test,y_train,y_test = clean_df(df)
    model = train_model(X_train,X_test,y_train,y_test,config=config)
    r2_score,rmse = evaluate_model(model,X_test,y_test)

