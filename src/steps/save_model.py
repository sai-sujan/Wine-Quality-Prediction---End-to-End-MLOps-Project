import pickle
import logging
import os
from sklearn.base import RegressorMixin
from zenml import step
from src.utils.s3_utils import S3Handler

@step
def save_model(model: RegressorMixin) -> None:
    """Save trained model to disk and optionally to S3"""
    try:
        # Always save locally first
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        logging.info("💾 Model saved to model.pkl")

        # Upload to S3 if configured
        if os.getenv('SAVE_TO_S3', 'false').lower() == 'true':
            s3_handler = S3Handler()

            # Upload model
            if s3_handler.upload_model('model.pkl'):
                logging.info("☁️  Model uploaded to S3")

            # Upload hyperparameters if they exist
            if os.path.exists('best_params.json'):
                if s3_handler.upload_params('best_params.json'):
                    logging.info("☁️  Hyperparameters uploaded to S3")

    except Exception as e:
        logging.error(f"Error saving model: {e}")
        raise e
