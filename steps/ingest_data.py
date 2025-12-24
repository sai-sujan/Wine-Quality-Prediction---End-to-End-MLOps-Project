import logging

import pandas as pd
from zenml import step

from .config import DataConfig


class IngestData:
    """
    Data ingestion class which ingests data from URL and returns a DataFrame.
    """

    def __init__(self, data_url: str, wine_type: str = "red") -> None:
        """
        Initialize the data ingestion class.

        Args:
            data_url: URL to fetch the wine quality dataset
            wine_type: Type of wine dataset ("red", "white", or "combined")
        """
        self.data_url = data_url
        self.wine_type = wine_type

    def get_data(self) -> pd.DataFrame:
        """
        Fetch data from URL and return as DataFrame.

        Returns:
            pd.DataFrame: Wine quality dataset
        """
        try:
            logging.info(f"Fetching {self.wine_type} wine data from URL: {self.data_url}")

            # Read CSV from URL with semicolon delimiter (UCI wine dataset uses semicolons)
            df = pd.read_csv(self.data_url, sep=';')

            # Add wine type column for tracking
            df['wine_type'] = self.wine_type

            logging.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
            logging.info(f"Columns: {list(df.columns)}")

            return df

        except Exception as e:
            logging.error(f"Error fetching data from {self.data_url}: {e}")
            raise e


@step
def ingest_df(config: DataConfig) -> pd.DataFrame:
    """
    Ingest wine quality data from URL.

    Args:
        config: DataConfig with data_url and wine_type

    Returns:
        df: pd.DataFrame containing wine quality data
    """
    try:
        # Handle combined dataset option
        if config.wine_type == "combined":
            # Fetch both red and white wine datasets
            red_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
            white_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"

            ingest_red = IngestData(red_url, "red")
            ingest_white = IngestData(white_url, "white")

            df_red = ingest_red.get_data()
            df_white = ingest_white.get_data()

            # Combine datasets
            df = pd.concat([df_red, df_white], ignore_index=True)
            logging.info(f"Combined dataset: {len(df)} total records")
        else:
            # Fetch single dataset
            ingest_data = IngestData(config.data_url, config.wine_type)
            df = ingest_data.get_data()

        return df

    except Exception as e:
        logging.error(f"Error in ingest_df step: {e}")
        raise e
