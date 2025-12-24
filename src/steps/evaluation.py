import logging
from zenml import step
import pandas as pd
from zenml.client import Client
from src.core.evaluation import MSE,R2Score,RMSE
from sklearn.base import RegressorMixin
from typing import Tuple
from typing_extensions import Annotated 
import mlflow

experiment_tracker = Client().active_stack.experiment_tracker
@step(experiment_tracker = experiment_tracker.name if experiment_tracker else None)
def evaluate_model(model:RegressorMixin,
                   X_test:pd.DataFrame,
                   y_test:pd.DataFrame) -> Tuple[Annotated[float,"r2score"],Annotated[float,"rmse"]] :
    """
    Evaluates the model on the ingested data.
    Agrs:
        df: the ingested data
    """
    try:
        prediction = model.predict(X_test)
        mse_class = MSE()
        mse = mse_class.calculate_score(y_test,prediction)
        mlflow.log_metric("mse",mse)

        # Using the R2Score class for R2 score calculation
        r2_class = R2Score()
        r2_score = r2_class.calculate_score(y_test, prediction)
        mlflow.log_metric("r2_score",r2_score)

        # Using the RMSE class for root mean squared error calculation
        rmse_class = RMSE()
        rmse = rmse_class.calculate_score(y_test, prediction)
        mlflow.log_metric("rmse",rmse)

        return r2_score,rmse
    except Exception as e:
        logging.error("Error in evaliuating the model: {}".format(e))
        raise e

