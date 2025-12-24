"""
AWS Lambda handler for Wine Quality Prediction
Loads model from S3 and serves predictions
"""
import json
import pickle
import os
import boto3
from typing import Dict, Any

# Global variables for model caching
model = None
s3_client = None

# Configuration
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'wine-quality-mlops-sujan')
MODEL_KEY = 'models/model.pkl'
REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-2')  # Lambda provides AWS_DEFAULT_REGION


def load_model_from_s3():
    """Download and load model from S3"""
    global model, s3_client

    if model is not None:
        return model

    try:
        # Initialize S3 client
        if s3_client is None:
            s3_client = boto3.client('s3', region_name=REGION)

        # Download model from S3 to /tmp
        local_model_path = '/tmp/model.pkl'
        s3_client.download_file(BUCKET_NAME, MODEL_KEY, local_model_path)
        print(f"✅ Downloaded model from s3://{BUCKET_NAME}/{MODEL_KEY}")

        # Load model
        with open(local_model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully")

        return model

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function

    Args:
        event: API Gateway event (contains request body)
        context: Lambda context

    Returns:
        API Gateway response with prediction
    """
    try:
        # Load model if not already loaded
        if model is None:
            load_model_from_s3()

        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})

        # Extract features as numpy array (avoids pandas dependency)
        import numpy as np
        features = np.array([[
            body.get('fixed_acidity'),
            body.get('volatile_acidity'),
            body.get('citric_acid'),
            body.get('residual_sugar'),
            body.get('chlorides'),
            body.get('free_sulfur_dioxide'),
            body.get('total_sulfur_dioxide'),
            body.get('density'),
            body.get('pH'),
            body.get('sulphates'),
            body.get('alcohol'),
            body.get('wine_type_encoded', 0)
        ]])

        # Make prediction
        prediction = model.predict(features)
        score = float(prediction[0])

        # Clip to valid range
        score = max(0, min(10, score))

        # Determine quality rating
        if score < 5:
            quality_rating = "Poor"
        elif score < 6:
            quality_rating = "Average"
        elif score < 7:
            quality_rating = "Good"
        else:
            quality_rating = "Excellent"

        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'prediction': score,
                'wine_quality_score': score,
                'quality_rating': quality_rating,
                'model_version': 'v1.0',
                'message': 'Prediction successful'
            })
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Prediction failed'
            })
        }


def health_check(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Health check endpoint for Lambda"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'wine-quality-predictor',
            'version': 'v1.0',
            'model_loaded': model is not None
        })
    }
