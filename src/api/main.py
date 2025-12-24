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
    title="Wine Quality Prediction API",
    description="MLOps project for predicting wine quality scores based on physicochemical properties",
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


# Request schema for Wine Quality Prediction
class PredictionRequest(BaseModel):
    fixed_acidity: float = Field(..., ge=0, description="Fixed acidity (tartaric acid - g/dm³)")
    volatile_acidity: float = Field(..., ge=0, description="Volatile acidity (acetic acid - g/dm³)")
    citric_acid: float = Field(..., ge=0, description="Citric acid (g/dm³)")
    residual_sugar: float = Field(..., ge=0, description="Residual sugar (g/dm³)")
    chlorides: float = Field(..., ge=0, description="Chlorides (sodium chloride - g/dm³)")
    free_sulfur_dioxide: float = Field(..., ge=0, description="Free sulfur dioxide (mg/dm³)")
    total_sulfur_dioxide: float = Field(..., ge=0, description="Total sulfur dioxide (mg/dm³)")
    density: float = Field(..., gt=0, description="Density (g/cm³)")
    pH: float = Field(..., ge=0, le=14, description="pH level")
    sulphates: float = Field(..., ge=0, description="Sulphates (potassium sulphate - g/dm³)")
    alcohol: float = Field(..., ge=0, description="Alcohol content (% by volume)")
    wine_type_encoded: Optional[int] = Field(0, ge=0, le=1, description="Wine type (0=red, 1=white)")

    class Config:
        schema_extra = {
            "example": {
                "fixed_acidity": 7.4,
                "volatile_acidity": 0.70,
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
            }
        }


# Response schema
class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Predicted wine quality score")
    wine_quality_score: float = Field(..., description="Wine quality (0-10)")
    quality_rating: str = Field(..., description="Quality rating (Poor/Average/Good/Excellent)")
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
        # Option 1: Try to load from root directory (saved by pipeline)
        root_model_path = "model.pkl"
        if os.path.exists(root_model_path):
            import pickle
            with open(root_model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Model loaded from: {root_model_path}")
            return model

        # Option 2: Try to load from models/ directory
        simple_model_path = "models/model.pkl"
        if os.path.exists(simple_model_path):
            import pickle
            with open(simple_model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Model loaded from: {simple_model_path}")
            return model

        # Option 3: Try to load from MLflow
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
        "message": "Wine Quality Prediction API",
        "description": "Predict wine quality scores (0-10) from physicochemical properties",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model/info",
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
        "service": "wine-quality-predictor",
        "version": "v1.0",
        "model_loaded": model_loaded
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """
    Make a prediction for wine quality

    Returns a score between 0-10 indicating predicted wine quality
    """
    try:
        # Load model if not already loaded
        if model is None:
            load_model()

        # Prepare features in the correct order
        features = pd.DataFrame([{
            'fixed acidity': request.fixed_acidity,
            'volatile acidity': request.volatile_acidity,
            'citric acid': request.citric_acid,
            'residual sugar': request.residual_sugar,
            'chlorides': request.chlorides,
            'free sulfur dioxide': request.free_sulfur_dioxide,
            'total sulfur dioxide': request.total_sulfur_dioxide,
            'density': request.density,
            'pH': request.pH,
            'sulphates': request.sulphates,
            'alcohol': request.alcohol,
            'wine_type_encoded': request.wine_type_encoded
        }])

        # Make prediction
        prediction = model.predict(features)
        score = float(prediction[0])

        # Clip to valid range (0-10)
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

        return {
            "prediction": score,
            "wine_quality_score": score,
            "quality_rating": quality_rating,
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
        "problem_type": "Wine Quality Prediction (Regression)",
        "target": "quality (0-10 score)",
        "features": [
            "fixed acidity",
            "volatile acidity",
            "citric acid",
            "residual sugar",
            "chlorides",
            "free sulfur dioxide",
            "total sulfur dioxide",
            "density",
            "pH",
            "sulphates",
            "alcohol",
            "wine_type_encoded"
        ],
        "version": "v1.0"
    }


if __name__ == "__main__":
    # Run the API server
    import sys
    from pathlib import Path

    # Add project root to Python path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    print("🚀 Starting Wine Quality Prediction API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    print("🍷 Predict wine quality from physicochemical properties")

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
