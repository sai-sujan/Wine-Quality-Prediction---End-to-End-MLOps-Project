"""
AWS Lambda function for model inference
Serves predictions via API Gateway
"""
import json
import os
import boto3
import mlflow
import numpy as np
import pandas as pd
from typing import Dict, Any


# Load model from S3 on cold start
s3_client = boto3.client('s3')
model = None
MODEL_BUCKET = os.environ.get('MODEL_BUCKET', 'your-mlflow-models')
MODEL_KEY = os.environ.get('MODEL_KEY', 'models/production/model')


def load_model():
    """Load model from S3"""
    global model
    if model is None:
        try:
            # Download model from S3
            local_path = '/tmp/model'
            s3_client.download_file(MODEL_BUCKET, MODEL_KEY, local_path)
            model = mlflow.sklearn.load_model(local_path)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return model


def validate_input(data: Dict[str, Any]) -> bool:
    """Validate input data"""
    required_features = [
        'payment_sequential',
        'payment_installments',
        'payment_value',
        'price',
        'freight_value',
        'product_name_lenght',
        'product_description_lenght',
        'product_photos_qty',
        'product_weight_g',
        'product_length_cm',
        'product_height_cm',
        'product_width_cm'
    ]

    return all(feature in data for feature in required_features)


def lambda_handler(event, context):
    """
    Lambda handler for model predictions

    Expected input:
    {
        "payment_sequential": 1,
        "payment_installments": 3,
        "payment_value": 100.0,
        ...
    }
    """

    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }

    try:
        # Parse input
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        # Validate input
        if not validate_input(body):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Missing required features',
                    'required': [
                        'payment_sequential',
                        'payment_installments',
                        'payment_value',
                        'price',
                        'freight_value',
                        'product_name_lenght',
                        'product_description_lenght',
                        'product_photos_qty',
                        'product_weight_g',
                        'product_length_cm',
                        'product_height_cm',
                        'product_width_cm'
                    ]
                })
            }

        # Load model
        model = load_model()

        # Prepare features
        features = pd.DataFrame([{
            'payment_sequential': body['payment_sequential'],
            'payment_installments': body['payment_installments'],
            'payment_value': body['payment_value'],
            'price': body['price'],
            'freight_value': body['freight_value'],
            'product_name_lenght': body['product_name_lenght'],
            'product_description_lenght': body['product_description_lenght'],
            'product_photos_qty': body['product_photos_qty'],
            'product_weight_g': body['product_weight_g'],
            'product_length_cm': body['product_length_cm'],
            'product_height_cm': body['product_height_cm'],
            'product_width_cm': body['product_width_cm']
        }])

        # Make prediction
        prediction = model.predict(features)

        # Return result
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'prediction': float(prediction[0]),
                'customer_satisfaction_score': float(prediction[0]),
                'model_version': os.environ.get('MODEL_VERSION', 'v1.0'),
                'message': 'Prediction successful'
            })
        }

    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# Health check endpoint
def health_check(event, context):
    """Health check endpoint"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'customer-satisfaction-predictor',
            'version': os.environ.get('MODEL_VERSION', 'v1.0')
        })
    }
