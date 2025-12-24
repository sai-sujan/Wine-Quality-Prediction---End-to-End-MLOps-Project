import boto3
import logging
import os
from botocore.exceptions import ClientError

class S3Handler:
    """Handle S3 operations for model and parameter storage"""

    def __init__(self, bucket_name: str = None, region: str = None):
        self.bucket_name = bucket_name or os.getenv('AWS_BUCKET_NAME', 'wine-quality-mlops-sujan')
        self.region = region or os.getenv('AWS_REGION', 'us-east-2')
        self.s3_client = boto3.client('s3', region_name=self.region)

    def upload_file(self, local_file: str, s3_key: str) -> bool:
        """Upload a file to S3"""
        try:
            self.s3_client.upload_file(local_file, self.bucket_name, s3_key)
            logging.info(f"✅ Uploaded {local_file} to s3://{self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            logging.error(f"❌ Failed to upload {local_file}: {e}")
            return False

    def download_file(self, s3_key: str, local_file: str) -> bool:
        """Download a file from S3"""
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_file)
            logging.info(f"✅ Downloaded s3://{self.bucket_name}/{s3_key} to {local_file}")
            return True
        except ClientError as e:
            logging.error(f"❌ Failed to download {s3_key}: {e}")
            return False

    def upload_model(self, model_path: str = "model.pkl") -> bool:
        """Upload model.pkl to S3"""
        s3_key = f"models/{model_path}"
        return self.upload_file(model_path, s3_key)

    def upload_params(self, params_path: str = "best_params.json") -> bool:
        """Upload best_params.json to S3"""
        s3_key = f"hyperparameters/{params_path}"
        return self.upload_file(params_path, s3_key)

    def download_model(self, local_path: str = "model.pkl") -> bool:
        """Download model.pkl from S3"""
        s3_key = f"models/{local_path}"
        return self.download_file(s3_key, local_path)

    def download_params(self, local_path: str = "best_params.json") -> bool:
        """Download best_params.json from S3"""
        s3_key = f"hyperparameters/{local_path}"
        return self.download_file(s3_key, local_path)
