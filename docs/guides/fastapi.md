# FastAPI Local Development Guide

## 🎯 Why FastAPI?

FastAPI provides **huge benefits** for your MLOps project:

### ✅ Advantages Over Lambda-Only Approach

| Feature | FastAPI (Local) | AWS Lambda Only |
|---------|----------------|-----------------|
| **Development Speed** | ⚡ Instant testing | ⏱️ Deploy to test |
| **Cost** | 💰 Free (local) | 💸 AWS charges |
| **Debugging** | 🐛 Easy debugging | 😓 CloudWatch logs |
| **Documentation** | 📖 Auto-generated | ❌ Manual |
| **Interactive Testing** | 🎮 Swagger UI | 🔧 curl/Postman |
| **Hot Reload** | ✅ Auto-refresh | ❌ Must redeploy |
| **Type Safety** | ✅ Pydantic validation | ⚠️ Manual checks |

### 🚀 Best of Both Worlds

```
Development (Local)          Production (AWS)
─────────────────           ────────────────
FastAPI on localhost   →    AWS Lambda
├─ Instant feedback         ├─ Auto-scaling
├─ Free to run              ├─ Pay per use
├─ Easy debugging           ├─ Global CDN
└─ Auto docs                └─ High availability
```

## 🏗️ Architecture

### Dual Deployment Strategy

```
┌──────────────────────────────────────────────┐
│  Same Code, Two Deployment Options          │
└──────────────────────────────────────────────┘

Development:                Production:
api.py (FastAPI)           lambda_function.py
    ↓                           ↓
localhost:8000             AWS Lambda + API Gateway
    ↓                           ↓
Your Machine               Cloud (Public URL)
```

Both use the **same model** and **same prediction logic**!

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Activate environment
source zenml_env/bin/activate

# Install FastAPI and uvicorn
pip install -r requirements.txt
```

### 2. Start the API

```bash
# Easy way
./run_api.sh

# Or manually
python api.py
```

### 3. Access the API

```
🌐 API: http://localhost:8000
📖 Docs: http://localhost:8000/docs (Swagger UI)
📚 ReDoc: http://localhost:8000/redoc (Alternative docs)
```

## 📖 Interactive Documentation

FastAPI automatically generates **beautiful, interactive API documentation**:

### Swagger UI (http://localhost:8000/docs)
- ✅ Try endpoints directly in browser
- ✅ See request/response schemas
- ✅ Auto-fills example data
- ✅ Download OpenAPI spec

### ReDoc (http://localhost:8000/redoc)
- ✅ Clean, professional documentation
- ✅ Code samples in multiple languages
- ✅ Perfect for sharing with team

## 🎮 Testing the API

### Option 1: Swagger UI (Easiest)

1. Open http://localhost:8000/docs
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Click "Execute"
5. See results instantly!

### Option 2: Python Script

```bash
python test_fastapi.py
```

### Option 3: cURL

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Option 4: Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
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
)

print(response.json())
```

## 📡 Available Endpoints

### 1. Root (`GET /`)
```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "Customer Satisfaction Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "predict": "/predict",
    "docs": "/docs",
    "redoc": "/redoc"
  }
}
```

### 2. Health Check (`GET /health`)
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "customer-satisfaction-predictor",
  "version": "v1.0",
  "model_loaded": true
}
```

### 3. Predict (`POST /predict`)
See examples above.

### 4. Model Info (`GET /model/info`)
```bash
curl http://localhost:8000/model/info
```

Response:
```json
{
  "model_type": "LinearRegression",
  "features": [...],
  "version": "v1.0"
}
```

## 🔄 Development Workflow

### Recommended Workflow

```bash
# 1. Train model
python run_pipeline.py

# 2. Start FastAPI (auto-reloads on code changes)
./run_api.sh

# 3. Test in browser
open http://localhost:8000/docs

# 4. Make changes to api.py
# API automatically reloads!

# 5. When ready, deploy to AWS
./deploy_aws.sh
```

## 🎯 Use Cases

### Local Development
```bash
# Start API
./run_api.sh

# Make code changes
# API auto-reloads (hot reload)

# Test immediately in browser
```

### Team Collaboration
```bash
# Share API docs
# Send link: http://your-ip:8000/docs

# Team can test without deploying
```

### Integration Testing
```python
# test_integration.py
import requests

def test_prediction_accuracy():
    response = requests.post(
        "http://localhost:8000/predict",
        json={...}
    )
    assert response.status_code == 200
    assert 0 <= response.json()["prediction"] <= 5
```

### Demo/Presentation
```bash
# Show live API during interview/presentation
# Interactive docs impress recruiters
open http://localhost:8000/docs
```

## 🆚 FastAPI vs AWS Lambda

### When to Use FastAPI (Local)

✅ **Development** - Fast iteration
✅ **Testing** - Instant feedback
✅ **Debugging** - Easy troubleshooting
✅ **Demos** - Show running API locally
✅ **Free** - No cloud costs

### When to Use AWS Lambda

✅ **Production** - Need 24/7 availability
✅ **Scalability** - Handle many users
✅ **Public Access** - Share with world
✅ **Portfolio** - Show on resume
✅ **Professional** - Enterprise deployment

### Best Practice: Use Both!

```
Development Cycle:
1. Develop with FastAPI (localhost)
2. Test with FastAPI (fast feedback)
3. Deploy to Lambda (production)
4. Share Lambda URL (public access)
```

## 🔧 Advanced Features

### Auto-Reload During Development

FastAPI watches for file changes:
```bash
# Start with auto-reload (default)
python api.py

# API reloads when you save changes to api.py!
```

### Input Validation

Pydantic automatically validates:
```python
# If you send invalid data:
{
  "payment_value": -100  # ❌ Must be > 0
}

# FastAPI returns helpful error:
{
  "detail": [
    {
      "loc": ["body", "payment_value"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

### Response Examples in Docs

Swagger UI shows example requests:
- Click any endpoint
- See pre-filled example
- Just click "Execute"!

## 📊 Comparison Summary

| Aspect | FastAPI | Lambda |
|--------|---------|--------|
| **Setup Time** | 30 seconds | 5 minutes |
| **Test Change** | Instant | 2-3 minutes |
| **Cost** | $0 | ~$0 (free tier) |
| **Documentation** | Auto-generated | Manual |
| **Public Access** | No (localhost) | Yes (AWS URL) |
| **Production Ready** | No | Yes |
| **Best For** | Development | Production |

## 🎓 Benefits for Your Portfolio

Having FastAPI shows:
- ✅ Modern Python skills
- ✅ API development expertise
- ✅ Best practices (validation, docs)
- ✅ Full-stack capabilities
- ✅ Professional development workflow

## 🚀 Next Steps

1. **Start FastAPI:**
   ```bash
   ./run_api.sh
   ```

2. **Explore docs:**
   ```
   http://localhost:8000/docs
   ```

3. **Test endpoints:**
   ```bash
   python test_fastapi.py
   ```

4. **Deploy to production:**
   ```bash
   ./deploy_aws.sh
   ```

## 💡 Pro Tips

1. **Keep FastAPI running during development** - Hot reload saves time
2. **Use Swagger UI for testing** - Faster than writing curl commands
3. **Share docs with team** - Professional API documentation
4. **Deploy Lambda for portfolio** - Public URL to showcase
5. **Use both** - FastAPI for dev, Lambda for prod

## ✅ Best Practice

```
✅ DO:
- Use FastAPI for local development
- Use Lambda for production/portfolio
- Keep code synchronized between both

❌ DON'T:
- Use FastAPI for production (use Lambda)
- Skip FastAPI (makes development slow)
- Expose localhost to internet
```

---

**You now have the best of both worlds:**
- 🚀 Fast local development with FastAPI
- ☁️ Professional cloud deployment with Lambda
- 📖 Auto-generated API documentation
- 🎯 Portfolio-ready project

Happy coding! 🎉
