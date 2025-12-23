"""
Simple training script that saves model directly for API use
"""
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

print("🚀 Starting simple model training...")

# Load data
print("📊 Loading data...")
df = pd.read_csv("data/olist_customers_dataset.csv")

# Select features and target
features = [
    'payment_sequential', 'payment_installments', 'payment_value',
    'price', 'freight_value', 'product_name_lenght',
    'product_description_lenght', 'product_photos_qty',
    'product_weight_g', 'product_length_cm', 'product_height_cm',
    'product_width_cm'
]

target = 'review_score'

# Clean data
print("🧹 Cleaning data...")
df = df.dropna(subset=[target])
df = df.dropna(subset=features)

X = df[features]
y = df[target]

# Split data
print("✂️  Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("🎓 Training model...")
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import mean_squared_error, r2_score
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"📈 Model Performance:")
print(f"   MSE: {mse:.4f}")
print(f"   R2 Score: {r2:.4f}")

# Save model
print("💾 Saving model...")
joblib.dump(model, "models/model.pkl")
print("✅ Model saved to models/model.pkl")

print("\n🎉 Training complete! You can now start the API with: ./run_api.sh")
