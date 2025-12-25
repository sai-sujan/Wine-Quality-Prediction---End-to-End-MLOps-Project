#!/bin/bash
set -e

echo "🧪 Testing Lambda Layer Build Locally"
echo "======================================"

# Create test directory
TEST_DIR="test_layer_local"
rm -rf $TEST_DIR
mkdir -p $TEST_DIR/python
cd $TEST_DIR/python

echo ""
echo "📦 Installing packages..."
pip3 install \
    scikit-learn \
    numpy \
    scipy \
    joblib \
    --target . \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.12 \
    --only-binary=:all: \
    --upgrade \
    -q 2>&1 | tail -5

echo ""
echo "🧹 Applying cleanup (from deploy script)..."
# Same cleanup as in deploy_lambda_with_layer.sh
rm -rf ./sklearn/tests 2>/dev/null || true
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyx" -delete 2>/dev/null || true
find . -name "*.c" -delete 2>/dev/null || true
find . -name "*.h" -delete 2>/dev/null || true
find . -name "*.md" -delete 2>/dev/null || true
rm -rf ./sklearn/datasets 2>/dev/null || true
# Only remove scipy modules that sklearn doesn't use
rm -rf ./scipy/tests 2>/dev/null || true
rm -rf ./scipy/integrate 2>/dev/null || true
rm -rf ./scipy/interpolate 2>/dev/null || true
rm -rf ./scipy/signal 2>/dev/null || true
rm -rf ./scipy/stats 2>/dev/null || true
rm -rf ./scipy/ndimage 2>/dev/null || true
rm -rf ./scipy/spatial 2>/dev/null || true

echo ""
echo "🔍 Checking numpy directory structure..."
echo ""
if [ -d "numpy" ]; then
    echo "Checking critical numpy subdirectories:"
    for dir in f2py _core; do
        if [ -d "numpy/$dir" ]; then
            echo "✅ numpy/$dir - EXISTS"
        else
            echo "❌ numpy/$dir - MISSING"
        fi
    done
else
    echo "❌ numpy directory not found!"
fi

echo ""
echo "🔍 Checking scipy directory structure..."
echo ""
if [ -d "scipy" ]; then
    echo "scipy/ critical modules:"
    for dir in linalg sparse special; do
        if [ -d "scipy/$dir" ]; then
            echo "✅ scipy/$dir - EXISTS"
        else
            echo "❌ scipy/$dir - MISSING (REQUIRED BY SKLEARN!)"
        fi
    done
else
    echo "❌ scipy directory not found!"
fi

echo ""
echo "📊 Layer size:"
du -sh . 2>/dev/null | cut -f1

cd ../..
rm -rf $TEST_DIR

echo ""
echo "✅ Test complete!"
