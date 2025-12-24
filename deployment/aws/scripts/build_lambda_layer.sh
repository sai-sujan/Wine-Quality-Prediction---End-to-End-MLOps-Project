#!/bin/bash
set -e

echo "🏗️  Building Lambda Layer for scikit-learn"
echo "=========================================="

LAYER_NAME="sklearn-numpy-scipy-layer"
REGION="us-east-2"
PYTHON_VERSION="3.12"

# Create layer directory structure
echo "📁 Creating layer directory structure..."
mkdir -p lambda_layer/python
cd lambda_layer/python

# Install dependencies for the layer
echo "📦 Installing scikit-learn, numpy, scipy, joblib..."
pip install \
    scikit-learn \
    numpy \
    scipy \
    joblib \
    --target . \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version $PYTHON_VERSION \
    --only-binary=:all: \
    --upgrade \
    -q

echo "✅ Dependencies installed"

# ULTRA aggressive cleanup for layer
echo "🧹 Cleaning up unnecessary files..."

# Remove test files and documentation
find . -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyx" -delete
find . -name "*.c" -delete
find . -name "*.h" -delete
find . -name "*.md" -delete
find . -name "*.txt" -delete

# Remove sklearn datasets and unnecessary modules
rm -rf ./sklearn/datasets 2>/dev/null || true
rm -rf ./sklearn/externals 2>/dev/null || true

# Remove numpy/scipy test files and docs
rm -rf ./numpy/tests 2>/dev/null || true
rm -rf ./numpy/doc 2>/dev/null || true
rm -rf ./numpy/f2py 2>/dev/null || true
rm -rf ./scipy/tests 2>/dev/null || true

# Remove scipy's large optional modules
rm -rf ./scipy/integrate 2>/dev/null || true
rm -rf ./scipy/interpolate 2>/dev/null || true
rm -rf ./scipy/signal 2>/dev/null || true
rm -rf ./scipy/stats 2>/dev/null || true
rm -rf ./scipy/ndimage 2>/dev/null || true
rm -rf ./scipy/spatial 2>/dev/null || true
rm -rf ./scipy/special 2>/dev/null || true
rm -rf ./scipy/io 2>/dev/null || true
rm -rf ./scipy/fft 2>/dev/null || true
rm -rf ./scipy/fftpack 2>/dev/null || true
rm -rf ./scipy/misc 2>/dev/null || true
rm -rf ./scipy/odr 2>/dev/null || true

# Remove joblib test files
rm -rf ./joblib/test 2>/dev/null || true

cd ..

# Check layer size
LAYER_SIZE=$(du -sh python | cut -f1)
echo "📏 Layer size: $LAYER_SIZE"

# Create zip file for layer
echo "🗜️  Creating layer zip..."
zip -r ../sklearn_layer.zip python -q

cd ..
rm -rf lambda_layer

LAYER_ZIP_SIZE=$(du -sh sklearn_layer.zip | cut -f1)
echo "✅ Layer zip created: sklearn_layer.zip ($LAYER_ZIP_SIZE)"
echo ""

# Upload layer to S3 (must be in S3 for layers > 50MB)
BUCKET_NAME="wine-quality-mlops-sujan"
LAYER_S3_KEY="lambda-layers/sklearn_layer_$(date +%Y%m%d_%H%M%S).zip"

echo "📤 Uploading layer to S3..."
aws s3 cp sklearn_layer.zip "s3://${BUCKET_NAME}/${LAYER_S3_KEY}" --region "$REGION"
echo "✅ Layer uploaded to s3://${BUCKET_NAME}/${LAYER_S3_KEY}"
echo ""

# Publish Lambda Layer from S3
echo "🚀 Publishing Lambda Layer..."
LAYER_VERSION_ARN=$(aws lambda publish-layer-version \
    --layer-name "$LAYER_NAME" \
    --description "Scikit-learn, NumPy, SciPy, Joblib for Python 3.12" \
    --content "S3Bucket=${BUCKET_NAME},S3Key=${LAYER_S3_KEY}" \
    --compatible-runtimes python3.12 \
    --region "$REGION" \
    --query 'LayerVersionArn' \
    --output text)

echo "✅ Layer published!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Lambda Layer Created Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Layer Name: $LAYER_NAME"
echo "🔗 Layer ARN: $LAYER_VERSION_ARN"
echo ""
echo "📝 Next: Update deploy_lambda.sh to use this layer ARN"
echo ""

# Save layer ARN to file for deploy_lambda.sh to use
echo "$LAYER_VERSION_ARN" > .lambda_layer_arn

# Cleanup
rm -f sklearn_layer.zip

echo "✅ Layer ARN saved to .lambda_layer_arn"
