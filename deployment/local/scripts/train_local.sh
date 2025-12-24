#!/bin/bash
set -e

echo "🏠 LOCAL Training - Model saved locally only"
echo "============================================="

# Activate virtual environment if it exists
if [ -d "zenml_env" ]; then
    source zenml_env/bin/activate
    echo "✅ Virtual environment activated"
fi

echo ""
echo "📦 Training model with local storage..."
echo "💾 Model will be saved to: model.pkl"
echo "💾 Parameters saved to: best_params.json"
echo ""

python scripts/run_local.py

echo ""
echo "✅ Local training complete!"
echo "📁 Model saved to: model.pkl"
echo ""
echo "Next steps:"
echo "  python src/api/main.py              - Start local API server"
echo "  streamlit run src/dashboard/streamlit_app.py  - Start Streamlit dashboard"
