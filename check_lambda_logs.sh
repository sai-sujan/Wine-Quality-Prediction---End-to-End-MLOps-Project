#!/bin/bash

FUNCTION_NAME="wine-quality-predictor"
REGION="us-east-2"

echo "🔍 Fetching latest Lambda logs..."

# Get the latest log stream
LOG_GROUP="/aws/lambda/${FUNCTION_NAME}"
LOG_STREAM=$(aws logs describe-log-streams \
    --log-group-name "$LOG_GROUP" \
    --region "$REGION" \
    --order-by LastEventTime \
    --descending \
    --max-items 1 \
    --query 'logStreams[0].logStreamName' \
    --output text)

if [ -z "$LOG_STREAM" ] || [ "$LOG_STREAM" = "None" ]; then
    echo "❌ No log streams found"
    exit 1
fi

echo "📋 Latest log stream: $LOG_STREAM"
echo ""
echo "📝 Recent logs:"
aws logs get-log-events \
    --log-group-name "$LOG_GROUP" \
    --log-stream-name "$LOG_STREAM" \
    --region "$REGION" \
    --limit 50 \
    --query 'events[*].message' \
    --output text
