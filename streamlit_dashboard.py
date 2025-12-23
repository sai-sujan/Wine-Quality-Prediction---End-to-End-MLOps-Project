"""
Simple Streamlit Dashboard for Customer Satisfaction Predictions
"""
import streamlit as st
import requests
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Customer Satisfaction Predictor",
    page_icon="🎯",
    layout="wide"
)

# Constants
FASTAPI_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🎯 Customer Satisfaction Predictor")
st.markdown("Predict customer satisfaction scores based on order details")
st.markdown("---")

# Check API status
def check_api_status():
    try:
        response = requests.get(f"{FASTAPI_URL}/health", timeout=2)
        if response.status_code == 200:
            return True
    except:
        return False

# Show API status
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if check_api_status():
        st.success("✅ Prediction API is running")
    else:
        st.error("❌ Prediction API is not running. Please start it with: ./run_api.sh")
        st.stop()

st.markdown("---")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Payment Information")
    payment_sequential = st.number_input("Payment Sequential", min_value=1, value=1, step=1)
    payment_installments = st.number_input("Payment Installments", min_value=1, value=3, step=1)
    payment_value = st.number_input("Payment Value ($)", min_value=0.01, value=142.90, step=0.01)
    price = st.number_input("Price ($)", min_value=0.01, value=129.99, step=0.01)
    freight_value = st.number_input("Freight Value ($)", min_value=0.0, value=12.91, step=0.01)

with col2:
    st.subheader("📦 Product Information")
    product_name_lenght = st.number_input("Product Name Length", min_value=1, value=58, step=1)
    product_description_lenght = st.number_input("Product Description Length", min_value=1, value=598, step=1)
    product_photos_qty = st.number_input("Product Photos Quantity", min_value=0, value=4, step=1)
    product_weight_g = st.number_input("Product Weight (g)", min_value=1, value=700, step=1)
    product_length_cm = st.number_input("Product Length (cm)", min_value=1, value=18, step=1)
    product_height_cm = st.number_input("Product Height (cm)", min_value=1, value=9, step=1)
    product_width_cm = st.number_input("Product Width (cm)", min_value=1, value=15, step=1)

st.markdown("---")

# Predict button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button("🔮 Predict Customer Satisfaction", use_container_width=True)

if predict_button:
    # Prepare data
    data = {
        "payment_sequential": int(payment_sequential),
        "payment_installments": int(payment_installments),
        "payment_value": float(payment_value),
        "price": float(price),
        "freight_value": float(freight_value),
        "product_name_lenght": int(product_name_lenght),
        "product_description_lenght": int(product_description_lenght),
        "product_photos_qty": int(product_photos_qty),
        "product_weight_g": int(product_weight_g),
        "product_length_cm": int(product_length_cm),
        "product_height_cm": int(product_height_cm),
        "product_width_cm": int(product_width_cm)
    }

    # Make prediction
    with st.spinner("Making prediction..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/predict", json=data)

            if response.status_code == 200:
                result = response.json()
                score = result.get("customer_satisfaction_score", result.get("prediction", 0))

                st.markdown("---")
                st.subheader("📊 Prediction Results")

                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Customer Satisfaction Score", 'font': {'size': 24}},
                    delta={'reference': 3.5, 'increasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 2.5], 'color': '#ffcccc'},
                            {'range': [2.5, 4], 'color': '#ffffcc'},
                            {'range': [4, 5], 'color': '#ccffcc'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 4.0
                        }
                    }
                ))

                fig.update_layout(
                    height=400,
                    margin=dict(l=20, r=20, t=50, b=20),
                    font={'size': 16}
                )

                st.plotly_chart(fig, use_container_width=True)

                # Interpretation
                col1, col2, col3 = st.columns(3)

                with col2:
                    if score >= 4.0:
                        st.success(f"😊 **High Satisfaction** - Score: {score:.2f}/5.0")
                        st.info("The customer is likely to be very satisfied with this order!")
                    elif score >= 2.5:
                        st.warning(f"😐 **Medium Satisfaction** - Score: {score:.2f}/5.0")
                        st.info("The customer satisfaction is average. Consider improvements.")
                    else:
                        st.error(f"😞 **Low Satisfaction** - Score: {score:.2f}/5.0")
                        st.info("The customer may not be satisfied. Review order details.")

            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.info("Make sure the FastAPI server is running: ./run_api.sh")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Customer Satisfaction Prediction System</p>
        <p>Powered by MLOps Pipeline (ZenML + MLflow + FastAPI)</p>
    </div>
""", unsafe_allow_html=True)
