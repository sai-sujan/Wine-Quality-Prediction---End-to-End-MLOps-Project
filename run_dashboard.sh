#!/bin/bash
set -e

echo "🎨 Starting Streamlit Production Dashboard"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d "zenml_env" ]; then
    source zenml_env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if Streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing Streamlit and dependencies..."
    pip install streamlit plotly pillow
fi

# Check if API is running
echo ""
echo "🔍 Checking if FastAPI is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI is running"
else
    echo "⚠️  Warning: FastAPI is not running"
    echo "💡 Start the API first for predictions to work:"
    echo "   ./run_api.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if MLflow UI is running
echo ""
echo "🔍 Checking if MLflow UI is running..."
if curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ MLflow UI is running"
else
    echo "⚠️  Warning: MLflow UI is not running"
    echo "💡 Start MLflow UI in a separate terminal:"
    echo "   source zenml_env/bin/activate"
    echo "   mlflow ui --backend-store-uri \"file:$HOME/Library/Application Support/zenml/local_stores/b368042e-441e-457a-92a6-cd3abc06cd3a/mlruns\""
    echo ""
fi

echo ""
echo "🎯 Starting Streamlit Dashboard..."
echo "🌐 Dashboard URL: http://localhost:8501"
echo ""
echo "📌 Dashboard Features:"
echo "   • 🔮 Make predictions"
echo "   • 🎓 Train models"
echo "   • 📊 View MLflow experiments"
echo "   • 🔄 Execute ZenML pipelines"
echo "   • 📈 Analytics and monitoring"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run the Streamlit app
streamlit run streamlit_dashboard.py
