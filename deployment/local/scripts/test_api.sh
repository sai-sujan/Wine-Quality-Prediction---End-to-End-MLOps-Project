#!/bin/bash

# Get API endpoint
STACK_NAME="customer-satisfaction-mlops"
AWS_REGION=$(aws configure get region || echo "us-east-1")

API_URL=$(aws cloudformation describe-stacks \
    --stack-name ${STACK_NAME} \
    --region ${AWS_REGION} \
    --query 'Stacks[0].Outputs[?OutputKey==`PredictionEndpoint`].OutputValue' \
    --output text 2>/dev/null)

if [ -z "$API_URL" ]; then
    echo "❌ API not deployed. Run ./deploy_aws.sh first"
    exit 1
fi

echo "🧪 Testing API: $API_URL"
echo ""

# Test prediction
curl -X POST $API_URL \
  -H 'Content-Type: application/json' \
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
  }' | python3 -m json.tool

echo ""
echo ""
echo "✅ Test complete!"
