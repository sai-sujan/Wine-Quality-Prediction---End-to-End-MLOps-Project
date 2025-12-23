from pipelines.training_pipeline import train_pipeline
from steps.config import ModelNameConfig

from zenml.client import Client
if __name__ =="__main__":
    # train_pipeline_path = "data/olist_customers_dataset.csv"
    print(Client().active_stack.experiment_tracker.get_tracking_uri())
    train_pipeline(config=ModelNameConfig(model_name="LinearRegressionModel"))

#mlflow ui --backend-store-uri "file:/Users/saisujan/Library/Application Support/zenml/local_stores/b368042e-441e-457a-92a6-cd3abc06cd3a/mlruns"    