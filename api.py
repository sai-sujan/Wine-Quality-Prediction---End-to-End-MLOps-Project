"""
FastAPI application for local development and testing
Serves the same endpoints as AWS Lambda
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import mlflow.sklearn
import pandas as pd
import os
from typing import Optional
import uvicorn


# Initialize FastAPI app
app = FastAPI(
    title="Customer Satisfaction Prediction API",
    description="MLOps project for predicting customer satisfaction scores",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None


# Request schema
class PredictionRequest(BaseModel):
    payment_sequential: int = Field(..., ge=1, description="Payment sequence number")
    payment_installments: int = Field(..., ge=1, description="Number of installments")
    payment_value: float = Field(..., gt=0, description="Total payment value")
    price: float = Field(..., gt=0, description="Product price")
    freight_value: float = Field(..., ge=0, description="Freight/shipping cost")
    product_name_lenght: int = Field(..., ge=0, description="Product name length")
    product_description_lenght: int = Field(..., ge=0, description="Product description length")
    product_photos_qty: int = Field(..., ge=0, description="Number of product photos")
    product_weight_g: float = Field(..., gt=0, description="Product weight in grams")
    product_length_cm: float = Field(..., gt=0, description="Product length in cm")
    product_height_cm: float = Field(..., gt=0, description="Product height in cm")
    product_width_cm: float = Field(..., gt=0, description="Product width in cm")

    class Config:
        schema_extra = {
            "example": {
                "payment_sequential": 1,
                "payment_installments": 3,
                "payment_value": 142.90,
                "price": 129.99,
                "freight_value": 12.91,
                "product_name_lenght": 58,
                "product_description_lenght": 598,
                "product_photos_qty": 4,
                "product_weight_g": 700,
                "product_length_cm": 18,
                "product_height_cm": 9,
                "product_width_cm": 15
            }
        }


# Response schema
class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted customer satisfaction score")
    customer_satisfaction_score: float = Field(..., description="Customer satisfaction (0-5)")
    model_version: str = Field(default="v1.0", description="Model version")
    message: str = Field(default="Prediction successful")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    model_loaded: bool


def load_model():
    """Load the latest trained model"""
    global model

    if model is not None:
        return model

    try:
        # Option 1: Try to load from models/ directory (simple training)
        simple_model_path = "models/model.pkl"
        if os.path.exists(simple_model_path):
            import joblib
            model = joblib.load(simple_model_path)
            print(f"✅ Model loaded from: {simple_model_path}")
            return model

        # Option 2: Try to load from MLflow
        mlflow_dir = os.path.expanduser(
            "~/Library/Application Support/zenml/local_stores/*/mlruns"
        )

        import glob
        mlrun_paths = glob.glob(mlflow_dir)

        if mlrun_paths:
            # Find latest model directory
            model_paths = []
            for mlrun_path in mlrun_paths:
                models = glob.glob(f"{mlrun_path}/*/*/artifacts/model")
                model_paths.extend(models)

            if model_paths:
                latest_model = max(model_paths, key=os.path.getmtime)
                model = mlflow.sklearn.load_model(latest_model)
                print(f"✅ Model loaded from MLflow: {latest_model}")
                return model

        raise FileNotFoundError("No trained model found")

    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("💡 Train a model first: python train_simple.py")
        raise


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        print("🚀 FastAPI server started successfully")
        print("📊 Model loaded and ready for predictions")
    except Exception as e:
        print(f"⚠️  Warning: Could not load model - {e}")
        print("   API will start but predictions will fail until model is trained")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Customer Satisfaction Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None

    return {
        "status": "healthy" if model_loaded else "degraded",
        "service": "customer-satisfaction-predictor",
        "version": "v1.0",
        "model_loaded": model_loaded
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Make a prediction for customer satisfaction

    Returns a score between 0-5 indicating predicted customer satisfaction
    """
    try:
        # Load model if not already loaded
        if model is None:
            load_model()

        # Prepare features
        features = pd.DataFrame([{
            'payment_sequential': request.payment_sequential,
            'payment_installments': request.payment_installments,
            'payment_value': request.payment_value,
            'price': request.price,
            'freight_value': request.freight_value,
            'product_name_lenght': request.product_name_lenght,
            'product_description_lenght': request.product_description_lenght,
            'product_photos_qty': request.product_photos_qty,
            'product_weight_g': request.product_weight_g,
            'product_length_cm': request.product_length_cm,
            'product_height_cm': request.product_height_cm,
            'product_width_cm': request.product_width_cm
        }])

        # Make prediction
        prediction = model.predict(features)
        score = float(prediction[0])

        # Clip to valid range (0-5)
        score = max(0, min(5, score))

        return {
            "prediction": score,
            "customer_satisfaction_score": score,
            "model_version": "v1.0",
            "message": "Prediction successful"
        }

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail="Model not found. Please train a model first using: python run_pipeline.py"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/model/info", tags=["Model"])
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="No model loaded"
        )

    return {
        "model_type": type(model).__name__,
        "features": [
            "payment_sequential",
            "payment_installments",
            "payment_value",
            "price",
            "freight_value",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ],
        "version": "v1.0"
    }


if __name__ == "__main__":
    # Run the API server
    print("🚀 Starting Customer Satisfaction Prediction API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
