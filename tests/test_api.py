import pytest
from fastapi.testclient import TestClient
import pickle
import os


@pytest.fixture(scope="module")
def test_client():
    """Create test client"""
    # Create a dummy model for testing
    from sklearn.ensemble import RandomForestRegressor
    import numpy as np

    model = RandomForestRegressor(n_estimators=10, random_state=42)
    X_dummy = np.random.rand(100, 12)
    y_dummy = np.random.rand(100) * 10

    model.fit(X_dummy, y_dummy)

    # Save dummy model
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)

    # Import and create client
    from api import app
    client = TestClient(app)

    yield client

    # Cleanup
    if os.path.exists('model.pkl'):
        os.remove('model.pkl')


def test_root_endpoint(test_client):
    """Test root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint(test_client):
    """Test health check"""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["service"] == "wine-quality-predictor"


def test_predict_endpoint(test_client):
    """Test prediction endpoint"""
    payload = {
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
    }

    response = test_client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "quality_rating" in data
    assert 0 <= data["wine_quality_score"] <= 10


def test_predict_invalid_data(test_client):
    """Test prediction with invalid data"""
    payload = {
        "fixed_acidity": "invalid",  # Should be float
    }

    response = test_client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error
