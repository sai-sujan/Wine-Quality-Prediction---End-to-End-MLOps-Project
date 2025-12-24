"""
Quick test script to verify wine quality data ingestion works
"""
import pandas as pd
from steps.ingest_data import IngestData

print("🧪 Testing Wine Quality Data Ingestion...\n")

try:
    # Test fetching red wine data
    print("1. Fetching red wine data from UCI repository...")
    ingest = IngestData(
        data_url="https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
        wine_type="red"
    )
    df = ingest.get_data()

    print(f"✅ Success! Loaded {len(df)} records")
    print(f"\n📊 Dataset Info:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"\n🔍 First few rows:")
    print(df.head(3))

    print(f"\n📈 Target variable (quality) distribution:")
    print(df['quality'].value_counts().sort_index())

    print(f"\n✨ Data ingestion is working correctly!")
    print(f"\n🚀 Next step: Run 'python run_pipeline.py' to train the model")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Troubleshooting:")
    print("   - Check your internet connection")
    print("   - Verify the UCI repository is accessible")
    print("   - Make sure pandas is installed")
