import logging
from abc import ABC, abstractmethod
import json
import os
from datetime import datetime

import optuna
import pandas as pd
import xgboost as xgb
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


class Model(ABC):
    """
    Abstract base class for all models.
    """

    @abstractmethod
    def train(self, x_train, y_train):
        """
        Trains the model on the given data.

        Args:
            x_train: Training data
            y_train: Target data
        """
        pass

    @abstractmethod
    def optimize(self, trial, x_train, y_train, x_test, y_test):
        """
        Optimizes the hyperparameters of the model.

        Args:
            trial: Optuna trial object
            x_train: Training data
            y_train: Target data
            x_test: Testing data
            y_test: Testing target
        """
        pass


class RandomForestModel(Model):
    """
    RandomForestModel that implements the Model interface.
    """

    def train(self, x_train, y_train, **kwargs):
        reg = RandomForestRegressor(**kwargs)
        reg.fit(x_train, y_train)
        return reg

    def optimize(self, trial, x_train, y_train, x_test, y_test):
        n_estimators = trial.suggest_int("n_estimators", 1, 200)
        max_depth = trial.suggest_int("max_depth", 1, 20)
        min_samples_split = trial.suggest_int("min_samples_split", 2, 20)
        reg = self.train(x_train, y_train, n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split)
        return reg.score(x_test, y_test)

class LightGBMModel(Model):
    """
    LightGBMModel that implements the Model interface.
    """

    def train(self, x_train, y_train, **kwargs):
        reg = LGBMRegressor(**kwargs)
        reg.fit(x_train, y_train)
        return reg

    def optimize(self, trial, x_train, y_train, x_test, y_test):
        n_estimators = trial.suggest_int("n_estimators", 1, 200)
        max_depth = trial.suggest_int("max_depth", 1, 20)
        learning_rate = trial.suggest_uniform("learning_rate", 0.01, 0.99)
        reg = self.train(x_train, y_train, n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
        return reg.score(x_test, y_test)


class XGBoostModel(Model):
    """
    XGBoostModel that implements the Model interface.
    """

    def train(self, x_train, y_train, **kwargs):
        reg = xgb.XGBRegressor(**kwargs)
        reg.fit(x_train, y_train)
        return reg

    def optimize(self, trial, x_train, y_train, x_test, y_test):
        n_estimators = trial.suggest_int("n_estimators", 1, 200)
        max_depth = trial.suggest_int("max_depth", 1, 30)
        learning_rate = trial.suggest_loguniform("learning_rate", 1e-7, 10.0)
        reg = self.train(x_train, y_train, n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)
        return reg.score(x_test, y_test)


class LinearRegressionModel(Model):
    """
    LinearRegressionModel that implements the Model interface.
    """

    def train(self, x_train, y_train, **kwargs):
        reg = LinearRegression(**kwargs)
        reg.fit(x_train, y_train)
        return reg

    # For linear regression, there might not be hyperparameters that we want to tune, so we can simply return the score
    def optimize(self, trial, x_train, y_train, x_test, y_test):
        reg = self.train(x_train, y_train)
        return reg.score(x_test, y_test)

class HyperparameterTuner:
    """
    Class for performing hyperparameter tuning. It uses Model strategy to perform tuning.
    Saves and loads best hyperparameters to avoid redundant optimization.
    """

    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.params_file = "best_params.json"

    def _get_model_name(self):
        """Get the model name for saving/loading parameters"""
        model_class_name = self.model.__class__.__name__
        name_mapping = {
            "RandomForestModel": "randomforest",
            "LightGBMModel": "lightgbm",
            "XGBoostModel": "xgboost",
            "LinearRegressionModel": "LinearRegressionModel"
        }
        return name_mapping.get(model_class_name, model_class_name)

    def _load_best_params(self):
        """Load previously saved best parameters for this model"""
        try:
            if os.path.exists(self.params_file):
                with open(self.params_file, 'r') as f:
                    all_params = json.load(f)
                model_name = self._get_model_name()
                params = all_params.get(model_name, {})
                if params:
                    logging.info(f"✅ Loaded saved hyperparameters for {model_name}: {params}")
                    return params
        except Exception as e:
            logging.warning(f"Could not load saved parameters: {e}")
        return None

    def _save_best_params(self, params):
        """Save the best parameters for this model"""
        try:
            # Load existing params
            if os.path.exists(self.params_file):
                with open(self.params_file, 'r') as f:
                    all_params = json.load(f)
            else:
                all_params = {
                    "randomforest": {},
                    "lightgbm": {},
                    "xgboost": {},
                    "LinearRegressionModel": {},
                    "last_updated": None
                }

            # Update with new params
            model_name = self._get_model_name()
            all_params[model_name] = params
            all_params["last_updated"] = datetime.now().isoformat()

            # Save to file
            with open(self.params_file, 'w') as f:
                json.dump(all_params, f, indent=2)

            logging.info(f"💾 Saved best hyperparameters for {model_name}: {params}")
        except Exception as e:
            logging.warning(f"Could not save parameters: {e}")

    def optimize(self, n_trials=100, use_cached=True):
        """
        Optimize hyperparameters using Optuna.

        Args:
            n_trials: Number of optimization trials
            use_cached: If True, use previously saved best parameters if available

        Returns:
            dict: Best hyperparameters
        """
        model_name = self._get_model_name()

        # Try to load cached parameters
        if use_cached:
            cached_params = self._load_best_params()
            if cached_params:
                logging.info(f"🚀 Using cached hyperparameters for {model_name} (skipping {n_trials} trials)")
                logging.info(f"   Set use_cached=False to run optimization again")
                return cached_params

        # Run optimization
        logging.info(f"🔬 Starting hyperparameter optimization for {model_name} ({n_trials} trials)...")
        study = optuna.create_study(direction="maximize")
        study.optimize(
            lambda trial: self.model.optimize(trial, self.x_train, self.y_train, self.x_test, self.y_test),
            n_trials=n_trials
        )

        best_params = study.best_trial.params
        best_score = study.best_trial.value

        logging.info(f"✨ Optimization complete!")
        logging.info(f"   Best R² Score: {best_score:.4f}")
        logging.info(f"   Best Parameters: {best_params}")

        # Save the best parameters
        self._save_best_params(best_params)

        return best_params
