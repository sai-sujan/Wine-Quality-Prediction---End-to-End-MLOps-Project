# 🚀 Quick Start Guide

Get your MLOps prediction system running in 2 minutes!

## 📋 Prerequisites

Make sure you have:
- ✅ Python 3.12 installed
- ✅ Virtual environment created (`zenml_env`)
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Model trained (`python run_pipeline.py`)

## ⚡ Quick Start (2 Terminals)

### Terminal 1: Start FastAPI

```bash
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project
./run_api.sh
```

**Access:** http://localhost:8000/docs

### Terminal 2: Start Streamlit Dashboard

```bash
cd /Users/saisujan/Desktop/interview_prep/mlops_prep/fcc_mlops_project
./run_dashboard.sh
```

**Access:** http://localhost:8501

---

## 🎯 What You Get

### Streamlit Dashboard (http://localhost:8501)
- 🔮 Make predictions with beautiful UI
- 📊 Gauge visualization of satisfaction scores
- ✅ Real-time API status check
- 💻 Clean, professional interface

### FastAPI Swagger (http://localhost:8000/docs)
- 📖 Interactive API documentation
- 🧪 Test endpoints directly
- 📝 View request/response schemas

---

## 🎬 Quick Demo

### Make a Prediction

1. Open http://localhost:8501
2. Fill in the form (or use default values)
3. Click "🔮 Predict Customer Satisfaction"
4. View the gauge chart and results!

### Example Values (Pre-filled)

```
Payment Sequential: 1
Payment Installments: 3
Payment Value: $142.90
Price: $129.99
Freight Value: $12.91
Product Name Length: 58
Product Description Length: 598
Product Photos Qty: 4
Product Weight: 700g
Product Length: 18cm
Product Height: 9cm
Product Width: 15cm
```

**Expected Result:** Score around 4.0-4.5 (High Satisfaction)

---

## 🛑 Stopping Services

Press `Ctrl+C` in each terminal.

Or kill all at once:

```bash
lsof -ti:8000 | xargs kill -9  # FastAPI
lsof -ti:8501 | xargs kill -9  # Streamlit
```

---

## 🐛 Troubleshooting

### "Port already in use"

```bash
# Check what's using the port
lsof -i:8000  # or :8501

# Kill the process
lsof -ti:8000 | xargs kill -9
```

### "Module not found"

```bash
# Make sure you're in the virtual environment
source zenml_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "No model found"

```bash
# Train a model first
python run_pipeline.py
```

### "API not responding" in Streamlit

```bash
# Make sure FastAPI is running in another terminal
./run_api.sh
```

---

## 🎓 First Time Setup

If this is your first time:

```bash
# 1. Setup environment
python3.12 -m venv zenml_env
source zenml_env/bin/activate
pip install -r requirements.txt

# 2. Initialize ZenML
zenml init
zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml stack register mlflow_stack -o default -a default -e mlflow_tracker
zenml stack set mlflow_stack

# 3. Train first model
python run_pipeline.py

# 4. Start services (in 2 terminals)
./run_api.sh          # Terminal 1
./run_dashboard.sh    # Terminal 2

# 5. Open dashboard
open http://localhost:8501
```

---

## 📱 Service Status Check

Check if services are running:

```bash
# Check FastAPI
curl -s http://localhost:8000/health

# Check Streamlit (if running, this will show HTML)
curl -s http://localhost:8501
```

---

## 🎯 Daily Development Workflow

```bash
# Quick start (in 2 terminals)
./run_api.sh          # Terminal 1
./run_dashboard.sh    # Terminal 2

# Open dashboard
open http://localhost:8501
```

---

## 🌟 What to Show Recruiters

### Demo Script (2 minutes)

```
1. Open Streamlit Dashboard (http://localhost:8501)
   "This is my customer satisfaction prediction system"

2. Show the form
   "Clean, professional interface for inputting order details"

3. Make a prediction
   "Real-time prediction with beautiful visualization"
   - Click "Predict Customer Satisfaction"
   - Show gauge chart
   - Explain the score (0-5 scale)

4. Show FastAPI docs (http://localhost:8000/docs)
   "Auto-generated API documentation"
   - Show the /predict endpoint
   - Try it out in Swagger

Result: Impressed recruiter! 🤩
```

---

## ☁️ Deploy to Production (Optional)

### Deploy FastAPI to AWS Lambda

```bash
./deploy_aws.sh
```

This gives you a public HTTPS endpoint!

### Deploy Streamlit to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Update `FASTAPI_URL` in streamlit_dashboard.py to your Lambda URL
5. Deploy!

Now anyone can access your prediction system! 🚀

---

## ✅ Checklist

Before demo:

- [ ] FastAPI running (http://localhost:8000)
- [ ] Streamlit running (http://localhost:8501)
- [ ] Model trained successfully
- [ ] Test prediction works
- [ ] No errors in terminal
- [ ] Ready to demo!

---

## 📚 Additional Resources

- **Streamlit Guide:** [STREAMLIT_SIMPLE_GUIDE.md](STREAMLIT_SIMPLE_GUIDE.md)
- **FastAPI Guide:** [FASTAPI_GUIDE.md](FASTAPI_GUIDE.md)
- **Main README:** [README.md](README.md)

---

**You're ready! 🎉**

Start with:
```bash
./run_api.sh          # Terminal 1
./run_dashboard.sh    # Terminal 2
```

Then open: http://localhost:8501
