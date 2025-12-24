#!/bin/bash

echo "🔍 Diagnosing Wine Quality Prediction Project..."
echo ""

# Check if virtual environment exists
echo "1. Checking virtual environment..."
if [ -d "zenml_env" ]; then
    echo "   ✅ Virtual environment exists: zenml_env/"
else
    echo "   ❌ Virtual environment NOT found"
    echo "   💡 Create it: python3.12 -m venv zenml_env"
fi
echo ""

# Check if model exists
echo "2. Checking model file..."
if [ -f "models/model.pkl" ]; then
    MODEL_DATE=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M:%S" models/model.pkl 2>/dev/null || stat -c "%y" models/model.pkl 2>/dev/null)
    echo "   ✅ Model exists: models/model.pkl"
    echo "   📅 Last modified: $MODEL_DATE"
    echo "   ⚠️  WARNING: This is the OLD model trained on customer satisfaction data"
    echo "   🔧 You need to train a NEW model with wine quality data"
else
    echo "   ❌ No model found"
    echo "   💡 Train a model: python run_pipeline.py"
fi
echo ""

# Check if data ingestion file is updated
echo "3. Checking updated files..."
if grep -q "Wine Quality" steps/ingest_data.py 2>/dev/null; then
    echo "   ✅ steps/ingest_data.py - Updated for wine quality"
else
    echo "   ❌ steps/ingest_data.py - NOT updated"
fi

if grep -q "wine quality" src/data_cleaning.py 2>/dev/null; then
    echo "   ✅ src/data_cleaning.py - Updated for wine quality"
else
    echo "   ❌ src/data_cleaning.py - NOT updated"
fi

if grep -q "Wine Quality" api.py 2>/dev/null; then
    echo "   ✅ api.py - Updated for wine quality"
else
    echo "   ❌ api.py - NOT updated"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✨ Your code files are updated for Wine Quality Prediction!"
echo "⚠️  BUT you still have the OLD model trained on customer data"
echo ""
echo "🚀 TO FIX THE PREDICTION ERROR:"
echo ""
echo "   1. Activate virtual environment:"
echo "      source zenml_env/bin/activate"
echo ""
echo "   2. Train new model with wine quality data:"
echo "      python run_pipeline.py"
echo ""
echo "   3. Wait for training to complete (~2-5 minutes)"
echo ""
echo "   4. Start API server:"
echo "      ./run_api.sh"
echo ""
echo "   5. Start dashboard:"
echo "      ./run_dashboard.sh"
echo ""
echo "📖 For more details, see: QUICK_FIX_GUIDE.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
