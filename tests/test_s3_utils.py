import pytest
from unittest.mock import Mock, patch
from src.utils.s3_utils import S3Handler


class TestS3Handler:
    """Test S3 utility functions"""

    @patch('boto3.client')
    def test_s3_handler_initialization(self, mock_boto_client):
        """Test S3Handler initialization"""
        handler = S3Handler()

        assert handler.bucket_name == 'wine-quality-mlops-sujan'
        assert handler.region == 'us-east-2'
        mock_boto_client.assert_called_once_with('s3', region_name='us-east-2')

    @patch('boto3.client')
    def test_upload_model_success(self, mock_boto_client):
        """Test successful model upload"""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        handler = S3Handler()

        # Mock file existence
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', create=True):
                result = handler.upload_file('model.pkl', 'models/model.pkl')

        assert result is True

    @patch('boto3.client')
    def test_download_model(self, mock_boto_client):
        """Test model download"""
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3

        handler = S3Handler()
        result = handler.download_file('models/model.pkl', 'model.pkl')

        # Should attempt download
        mock_s3.download_file.assert_called_once()
