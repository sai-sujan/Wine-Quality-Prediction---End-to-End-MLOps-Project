# 🎯 Simple Streamlit Prediction Dashboard

## Overview

A clean, simple Streamlit dashboard for making customer satisfaction predictions. No training, no MLflow integration - **just predictions**.

## ✨ Features

- ✅ Simple prediction form
- ✅ Beautiful gauge visualization
- ✅ Real-time API status check
- ✅ Clean, professional UI
- ✅ Easy to use

## 🚀 Quick Start

### 1. Start FastAPI (required)

```bash
./run_api.sh
```

### 2. Start Streamlit Dashboard

```bash
./run_dashboard.sh
```

### 3. Open in Browser

```
http://localhost:8501
```

## 📖 How to Use

1. **Check API Status** - Green checkmark means API is running
2. **Fill in Payment Information:**
   - Payment Sequential
   - Payment Installments
   - Payment Value
   - Price
   - Freight Value

3. **Fill in Product Information:**
   - Product Name Length
   - Product Description Length
   - Product Photos Quantity
   - Product Weight
   - Product Dimensions (length, height, width)

4. **Click "Predict Customer Satisfaction"**

5. **View Results:**
   - Gauge chart showing satisfaction score (0-5)
   - Color-coded interpretation:
     - 🟢 Green (4-5): High Satisfaction
     - 🟡 Yellow (2.5-4): Medium Satisfaction
     - 🔴 Red (0-2.5): Low Satisfaction

## 🎨 What You See

### Dashboard Layout

```
┌─────────────────────────────────────────────┐
│  🎯 Customer Satisfaction Predictor         │
│  Predict customer satisfaction scores       │
├─────────────────────────────────────────────┤
│  ✅ Prediction API is running               │
├─────────────────────────────────────────────┤
│  💳 Payment Info    │  📦 Product Info      │
│  ├─ Sequential      │  ├─ Name Length       │
│  ├─ Installments    │  ├─ Description Len   │
│  ├─ Payment Value   │  ├─ Photos Qty        │
│  ├─ Price           │  ├─ Weight (g)        │
│  └─ Freight Value   │  ├─ Length (cm)       │
│                     │  ├─ Height (cm)       │
│                     │  └─ Width (cm)        │
├─────────────────────────────────────────────┤
│      🔮 Predict Customer Satisfaction       │
├─────────────────────────────────────────────┤
│  📊 Prediction Results                      │
│                                             │
│        ┌─────────────────────┐             │
│        │   Gauge Chart       │             │
│        │   Score: 4.2/5.0    │             │
│        └─────────────────────┘             │
│                                             │
│  😊 High Satisfaction - Score: 4.20/5.0    │
│  The customer is likely to be very          │
│  satisfied with this order!                 │
└─────────────────────────────────────────────┘
```

## 📊 Example Prediction

### Input Values

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

### Expected Output

- **Score:** ~4.2/5.0
- **Status:** 😊 High Satisfaction
- **Message:** "The customer is likely to be very satisfied with this order!"

## 🔧 Configuration

### Change API URL

If your FastAPI is running on a different URL, edit [streamlit_dashboard.py](streamlit_dashboard.py:17):

```python
FASTAPI_URL = "http://localhost:8000"  # Change this
```

### Change Port

Default Streamlit port is 8501. To change:

```bash
streamlit run streamlit_dashboard.py --server.port 8502
```

## 🐛 Troubleshooting

### "Prediction API is not running"

**Problem:** Red error message at the top

**Solution:**
```bash
# Start FastAPI in another terminal
./run_api.sh
```

### "Error making prediction"

**Problem:** Error when clicking predict button

**Solutions:**
1. Check FastAPI is running: `curl http://localhost:8000/health`
2. Restart FastAPI: Stop it (Ctrl+C) and run `./run_api.sh` again
3. Check all input values are valid (no negative numbers, etc.)

### Port 8501 already in use

**Problem:** Can't start Streamlit

**Solution:**
```bash
# Kill existing Streamlit process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run streamlit_dashboard.py --server.port 8502
```

### Module not found errors

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
source zenml_env/bin/activate
pip install streamlit plotly
```

## 🎯 Use Cases

### 1. Quick Prediction
- Fill form with customer order data
- Click predict
- Get instant satisfaction score

### 2. Batch Testing
- Enter different product configurations
- Compare satisfaction scores
- Find optimal pricing/product combinations

### 3. Demo to Stakeholders
- Clean, professional interface
- Easy to understand gauge visualization
- No technical knowledge required

## 💡 Tips

1. **Default values are pre-filled** - You can click predict immediately to see it work
2. **Gauge is color-coded** - Red (low), Yellow (medium), Green (high)
3. **API must be running** - Dashboard checks this automatically
4. **Use realistic values** - Model trained on real e-commerce data

## 🚀 Deployment Options

### Local Only (Current)
```bash
./run_api.sh        # Terminal 1
./run_dashboard.sh  # Terminal 2
```
Access: http://localhost:8501

### Deploy to Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

**Note:** You'll need to modify the dashboard to use your deployed FastAPI URL instead of localhost.

### Deploy with FastAPI to Cloud

If you deploy FastAPI to AWS Lambda:

1. Get your API Gateway URL from AWS deployment
2. Edit `streamlit_dashboard.py`:
   ```python
   FASTAPI_URL = "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod"
   ```
3. Deploy Streamlit to Streamlit Cloud
4. Anyone can access it!

## 📚 What's Next?

### Current Setup
- ✅ FastAPI (local) for predictions
- ✅ Streamlit (local) for UI
- ✅ Simple prediction interface

### Optional Enhancements
- Deploy FastAPI to AWS Lambda (already set up!)
- Deploy Streamlit to Streamlit Cloud (free)
- Add prediction history
- Add batch upload (CSV file)
- Add download results feature

## ✅ Summary

You now have:
- ✅ **Simple prediction UI** (Streamlit)
- ✅ **Clean, professional design**
- ✅ **Easy to use** - No technical knowledge needed
- ✅ **Beautiful visualization** - Gauge chart
- ✅ **Real-time status check** - Knows if API is running

**Start it:**
```bash
# Terminal 1
./run_api.sh

# Terminal 2
./run_dashboard.sh
```

**Use it:**
```
http://localhost:8501
```

That's it! Simple and focused on predictions only. 🎯
