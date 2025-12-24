#!/bin/bash
set -e

echo "🚀 Starting FastAPI Server for Local Development"
echo "================================================"

# Activate virtual environment if it exists
if [ -d "zenml_env" ]; then
    source zenml_env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing FastAPI and dependencies..."
    pip install fastapi uvicorn[standard] pydantic
fi

# Check if model exists
if [ ! -d "$HOME/Library/Application Support/zenml" ]; then
    echo "⚠️  Warning: No trained model found"
    echo "💡 Train a model first:"
    echo "   python scripts/run_local.py"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🎯 Starting API server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔧 Alternative docs: http://localhost:8000/redoc"
echo "💻 API endpoint: http://localhost:8000/predict"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the API
python src/api/main.py
