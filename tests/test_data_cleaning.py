import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import DataPreProcessingStrategy, DataDivideStrategy


class TestDataPreProcessingStrategy:
    """Test data preprocessing"""

    def test_handle_data_removes_duplicates(self):
        # Create sample data with duplicates
        data = pd.DataFrame({
            'fixed acidity': [7.4, 7.4, 7.8],
            'volatile acidity': [0.7, 0.7, 0.6],
            'quality': [5, 5, 6]
        })

        strategy = DataPreProcessingStrategy()
        result = strategy.handle_data(data)

        assert len(result) == 2  # One duplicate removed

    def test_handle_data_drops_non_numeric(self):
        # Create data with non-numeric columns
        data = pd.DataFrame({
            'fixed acidity': [7.4, 7.8],
            'quality': [5, 6],
            'wine_type': ['red', 'white']
        })

        strategy = DataPreProcessingStrategy()
        result = strategy.handle_data(data)

        assert 'wine_type' not in result.columns


class TestDataDivideStrategy:
    """Test train/test split"""

    def test_divide_data_split_ratio(self):
        # Create sample data
        data = pd.DataFrame({
            'fixed acidity': np.random.rand(100),
            'volatile acidity': np.random.rand(100),
            'quality': np.random.randint(3, 9, 100)
        })

        strategy = DataDivideStrategy()
        X_train, X_test, y_train, y_test = strategy.handle_data(data)

        # Check 80-20 split
        assert len(X_train) == 80
        assert len(X_test) == 20
        assert len(y_train) == 80
        assert len(y_test) == 20

    def test_divide_data_target_column(self):
        # Create sample data
        data = pd.DataFrame({
            'fixed acidity': [7.4, 7.8, 8.0],
            'quality': [5, 6, 7]
        })

        strategy = DataDivideStrategy()
        X_train, X_test, y_train, y_test = strategy.handle_data(data)

        # Ensure quality column is the target
        assert 'quality' not in X_train.columns
        assert 'quality' not in X_test.columns
