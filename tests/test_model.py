import pytest
import numpy as np
import pandas as pd
from src.core.model_dev import RandomForestModel, LinearRegressionModel, HyperparameterTuner


class TestRandomForestModel:
    """Test RandomForest model"""

    def test_train_model(self):
        # Create sample data
        X_train = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100)
        })
        y_train = pd.Series(np.random.randint(3, 9, 100))

        model = RandomForestModel()
        trained_model = model.train(X_train, y_train)

        assert trained_model is not None
        assert hasattr(trained_model, 'predict')

    def test_model_prediction(self):
        # Create sample data
        X_train = pd.DataFrame({
            'feature1': np.random.rand(100),
            'feature2': np.random.rand(100)
        })
        y_train = pd.Series(np.random.randint(3, 9, 100))

        model = RandomForestModel()
        trained_model = model.train(X_train, y_train)

        # Test prediction
        X_test = pd.DataFrame({
            'feature1': [0.5],
            'feature2': [0.5]
        })
        prediction = trained_model.predict(X_test)

        assert len(prediction) == 1
        assert 0 <= prediction[0] <= 10


class TestLinearRegressionModel:
    """Test Linear Regression model"""

    def test_train_model(self):
        X_train = pd.DataFrame({
            'feature1': np.random.rand(50),
            'feature2': np.random.rand(50)
        })
        y_train = pd.Series(np.random.rand(50) * 10)

        model = LinearRegressionModel()
        trained_model = model.train(X_train, y_train)

        assert trained_model is not None
        assert hasattr(trained_model, 'predict')


class TestHyperparameterTuner:
    """Test hyperparameter optimization"""

    def test_load_cached_params(self):
        X_train = pd.DataFrame({'f1': np.random.rand(50)})
        y_train = pd.Series(np.random.randint(3, 9, 50))
        X_test = pd.DataFrame({'f1': np.random.rand(20)})
        y_test = pd.Series(np.random.randint(3, 9, 20))

        model = RandomForestModel()
        tuner = HyperparameterTuner(model, X_train, y_train, X_test, y_test)

        # Should return None if no cached params
        cached = tuner._load_best_params()
        assert cached is None or isinstance(cached, dict)
