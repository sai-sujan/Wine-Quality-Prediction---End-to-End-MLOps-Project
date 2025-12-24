import pytest
from unittest.mock import Mock, patch
import json


class TestLambdaHandler:
    """Test Lambda handler functions"""

    @patch('lambda_handler.load_model_from_s3')
    @patch('lambda_handler.model')
    def test_lambda_handler_success(self, mock_model, mock_load_model):
        """Test successful prediction"""
        from lambda_handler import lambda_handler

        # Mock model prediction
        mock_model_instance = Mock()
        mock_model_instance.predict.return_value = [6.5]
        mock_load_model.return_value = mock_model_instance

        # Create test event
        event = {
            'body': json.dumps({
                "fixed_acidity": 7.4,
                "volatile_acidity": 0.7,
                "citric_acid": 0.0,
                "residual_sugar": 1.9,
                "chlorides": 0.076,
                "free_sulfur_dioxide": 11.0,
                "total_sulfur_dioxide": 34.0,
                "density": 0.9978,
                "pH": 3.51,
                "sulphates": 0.56,
                "alcohol": 9.4,
                "wine_type_encoded": 0
            })
        }
        context = {}

        # Call handler
        with patch('lambda_handler.model', mock_model_instance):
            response = lambda_handler(event, context)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'prediction' in body
        assert 'quality_rating' in body

    def test_health_check(self):
        """Test health check endpoint"""
        from lambda_handler import health_check

        event = {}
        context = {}

        response = health_check(event, context)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['service'] == 'wine-quality-predictor'
