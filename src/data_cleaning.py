import logging
from abc import ABC,abstractmethod 
from typing import Union,Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from typing_extensions import Annotated

class Datastrategy(ABC):
    """
    Abstract class defiininng strategy for handling data
    """

    @abstractmethod
    def handle_data(self,data:pd.DataFrame) -> Union[pd.DataFrame,pd.Series]:
        pass

class DataPreProcessingStrategy(Datastrategy):
    """
    Strategy for preprocessing data
    """
    def handle_data(self,data:pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data
        """
        try:
            data = data.drop(
                [
                   "order_approved_at",
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                    "order_estimated_delivery_date",
                    "order_purchase_timestamp",
                ],
                axis=1
            )
            data["product_weight_g"].fillna(data["product_weight_g"].median(), inplace=True)
            data["product_length_cm"].fillna(data["product_length_cm"].median(), inplace=True)
            data["product_height_cm"].fillna(data["product_height_cm"].median(), inplace=True)
            data["product_width_cm"].fillna(data["product_width_cm"].median(), inplace=True)
            # write "No review" in review_comment_message column
            data["review_comment_message"].fillna("No review", inplace=True)

            data = data.select_dtypes(include=[np.number])
            cols_to_drop = ["customer_zip_code_prefix", "order_item_id"]
            data = data.drop(cols_to_drop, axis=1)

            return data
        except Exception as e:
            logging.error(e)
            raise e
        
class DataDivideStrategy(Datastrategy):
    """Strategy to divide data into train/test"""
    
    def handle_data(self, data: pd.DataFrame) -> Tuple[Annotated[pd.DataFrame,"X_train"], Annotated[pd.DataFrame,"X_test"], Annotated[pd.Series,"y_train"],Annotated[pd.Series,"y_test"]]:
        try:
            X = data.drop("review_score", axis=1)
            y = data["review_score"]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Force ZenML-compatible types
            X_train = pd.DataFrame(X_train, columns=X.columns)
            X_test = pd.DataFrame(X_test, columns=X.columns)
            y_train = pd.Series(y_train, name="review_score")
            y_test = pd.Series(y_test, name="review_score")
            
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(e)
            raise e

class DataCleaning:
    """
    Class for cleaning data which process the data and divides it into train and test
    """
    def __init__(self,data:pd.DataFrame,strategy:Datastrategy):
        self.data = data
        self.strategy = strategy
    
    def handle_data(self) -> Union[pd.DataFrame,pd.Series]:
        """Handle data"""
        try:
            return self.strategy.handle_data(self.data)     
        except Exception as e:
            logging.error("Errror in handling data: {}".format(e)) 
            raise e  
