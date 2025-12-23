"""
Test script for FastAPI local development
"""
import requests
import json


def test_api():
    """Test the FastAPI endpoints"""
    base_url = "http://localhost:8000"

    print("🧪 Testing Customer Satisfaction Prediction API")
    print("=" * 50)

    # Test 1: Root endpoint
    print("\n1️⃣  Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Health check
    print("\n2️⃣  Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Prediction
    print("\n3️⃣  Testing prediction endpoint...")
    data = {
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

    try:
        response = requests.post(f"{base_url}/predict", json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Request: {json.dumps(data, indent=2)}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            score = response.json()["customer_satisfaction_score"]
            print(f"\n   ✅ Prediction successful!")
            print(f"   📊 Customer Satisfaction Score: {score:.2f}/5.0")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 4: Model info
    print("\n4️⃣  Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/model/info")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            info = response.json()
            print(f"   Model Type: {info['model_type']}")
            print(f"   Features: {len(info['features'])} features")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)
    print("✅ API testing complete!")
    print("\n💡 View interactive docs at: http://localhost:8000/docs")


if __name__ == "__main__":
    print("Make sure the API is running first:")
    print("  ./run_api.sh")
    print("\nStarting tests in 3 seconds...")

    import time
    time.sleep(3)

    test_api()
