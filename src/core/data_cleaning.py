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
    Strategy for preprocessing wine quality data
    """
    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess wine quality data.

        The wine quality dataset has the following features:
        - fixed acidity
        - volatile acidity
        - citric acid
        - residual sugar
        - chlorides
        - free sulfur dioxide
        - total sulfur dioxide
        - density
        - pH
        - sulphates
        - alcohol
        - quality (target variable)
        - wine_type (added during ingestion)
        """
        try:
            logging.info(f"Starting preprocessing. Dataset shape: {data.shape}")
            logging.info(f"Columns: {list(data.columns)}")

            # Check for missing values
            missing_values = data.isnull().sum()
            if missing_values.any():
                logging.warning(f"Found missing values: {missing_values[missing_values > 0]}")
                # Fill missing values with median for numeric columns
                numeric_columns = data.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    if data[col].isnull().any():
                        data[col].fillna(data[col].median(), inplace=True)

            # Encode wine_type if present (red=0, white=1)
            if 'wine_type' in data.columns:
                data['wine_type_encoded'] = data['wine_type'].map({'red': 0, 'white': 1})
                data = data.drop('wine_type', axis=1)
                logging.info("Encoded wine_type column")

            # Ensure all columns are numeric
            data = data.select_dtypes(include=[np.number])

            # Remove any duplicate rows
            initial_rows = len(data)
            data = data.drop_duplicates()
            removed_duplicates = initial_rows - len(data)
            if removed_duplicates > 0:
                logging.info(f"Removed {removed_duplicates} duplicate rows")

            logging.info(f"Preprocessing complete. Final shape: {data.shape}")
            logging.info(f"Final columns: {list(data.columns)}")

            return data
        except Exception as e:
            logging.error(f"Error in preprocessing: {e}")
            raise e
        
class DataDivideStrategy(Datastrategy):
    """Strategy to divide wine quality data into train/test"""

    def handle_data(self, data: pd.DataFrame) -> Tuple[Annotated[pd.DataFrame,"X_train"], Annotated[pd.DataFrame,"X_test"], Annotated[pd.Series,"y_train"],Annotated[pd.Series,"y_test"]]:
        """
        Split wine quality data into training and testing sets.

        Target variable: 'quality' (wine quality score from 0-10)
        """
        try:
            # The target variable for wine quality dataset is 'quality'
            X = data.drop("quality", axis=1)
            y = data["quality"]

            logging.info(f"Splitting data: Features shape: {X.shape}, Target shape: {y.shape}")
            logging.info(f"Feature columns: {list(X.columns)}")
            logging.info(f"Target value distribution:\n{y.value_counts().sort_index()}")

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Force ZenML-compatible types
            X_train = pd.DataFrame(X_train, columns=X.columns)
            X_test = pd.DataFrame(X_test, columns=X.columns)
            y_train = pd.Series(y_train, name="quality")
            y_test = pd.Series(y_test, name="quality")

            logging.info(f"Train set: {len(X_train)} samples, Test set: {len(X_test)} samples")

            return X_train, X_test, y_train, y_test
        except Exception as e:
            logging.error(f"Error in data splitting: {e}")
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
