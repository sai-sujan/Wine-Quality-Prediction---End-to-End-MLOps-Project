"""
Simple Streamlit Dashboard for Wine Quality Predictions
"""
import streamlit as st
import requests
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Wine Quality Predictor",
    page_icon="🍷",
    layout="wide"
)

# API Configuration - supports both local and AWS Lambda
DEFAULT_LOCAL_URL = "http://localhost:8000"
DEFAULT_AWS_URL = os.getenv("AWS_LAMBDA_URL", "")  # Set via environment variable

# Sidebar for API endpoint selection
with st.sidebar:
    st.header("⚙️ Settings")
    api_mode = st.radio(
        "API Endpoint",
        ["Local Development", "AWS Lambda"],
        help="Choose between local API or deployed AWS Lambda"
    )

    if api_mode == "Local Development":
        FASTAPI_URL = st.text_input(
            "Local API URL",
            value=DEFAULT_LOCAL_URL,
            help="URL of your local FastAPI server"
        )
    else:
        FASTAPI_URL = st.text_input(
            "AWS Lambda URL",
            value=DEFAULT_AWS_URL,
            placeholder="https://your-lambda-id.execute-api.us-east-2.amazonaws.com/prod",
            help="Your AWS Lambda API Gateway endpoint"
        )

    st.markdown("---")
    st.markdown("**Current Endpoint:**")
    st.code(FASTAPI_URL, language="text")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #8B0000;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #A52A2A;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🍷 Wine Quality Predictor")
st.markdown("Predict wine quality scores (0-10) based on physicochemical properties")
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
        st.success(f"✅ API is running ({api_mode})")
    else:
        st.error(f"❌ API is not reachable at: {FASTAPI_URL}")
        if api_mode == "Local Development":
            st.info("💡 Start local API: python src/api/main.py")
        else:
            st.info("💡 Check your AWS Lambda URL and ensure it's deployed")
        st.stop()

st.markdown("---")

# Wine type selector
wine_type = st.radio("🍷 Select Wine Type", ["Red Wine", "White Wine"], horizontal=True)
wine_type_encoded = 0 if wine_type == "Red Wine" else 1

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧪 Acidity & Chemical Properties")
    fixed_acidity = st.number_input(
        "Fixed Acidity (g/dm³)",
        min_value=0.0,
        max_value=20.0,
        value=7.4,
        step=0.1,
        help="Tartaric acid concentration"
    )
    volatile_acidity = st.number_input(
        "Volatile Acidity (g/dm³)",
        min_value=0.0,
        max_value=2.0,
        value=0.70,
        step=0.01,
        help="Acetic acid concentration"
    )
    citric_acid = st.number_input(
        "Citric Acid (g/dm³)",
        min_value=0.0,
        max_value=2.0,
        value=0.0,
        step=0.01,
        help="Adds freshness and flavor"
    )
    pH = st.number_input(
        "pH Level",
        min_value=2.0,
        max_value=5.0,
        value=3.51,
        step=0.01,
        help="Acidity level (lower = more acidic)"
    )

    st.subheader("🧂 Sugar & Minerals")
    residual_sugar = st.number_input(
        "Residual Sugar (g/dm³)",
        min_value=0.0,
        max_value=20.0,
        value=1.9,
        step=0.1,
        help="Sugar remaining after fermentation"
    )
    chlorides = st.number_input(
        "Chlorides (g/dm³)",
        min_value=0.0,
        max_value=1.0,
        value=0.076,
        step=0.001,
        help="Salt content"
    )
    sulphates = st.number_input(
        "Sulphates (g/dm³)",
        min_value=0.0,
        max_value=2.0,
        value=0.56,
        step=0.01,
        help="Wine additive (antimicrobial & antioxidant)"
    )

with col2:
    st.subheader("💨 Sulfur Dioxide & Density")
    free_sulfur_dioxide = st.number_input(
        "Free Sulfur Dioxide (mg/dm³)",
        min_value=0.0,
        max_value=100.0,
        value=11.0,
        step=1.0,
        help="Free form of SO₂"
    )
    total_sulfur_dioxide = st.number_input(
        "Total Sulfur Dioxide (mg/dm³)",
        min_value=0.0,
        max_value=300.0,
        value=34.0,
        step=1.0,
        help="Total SO₂ (free + bound forms)"
    )
    density = st.number_input(
        "Density (g/cm³)",
        min_value=0.9,
        max_value=1.1,
        value=0.9978,
        step=0.0001,
        help="Wine density"
    )

    st.subheader("🍇 Alcohol Content")
    alcohol = st.number_input(
        "Alcohol (% vol)",
        min_value=8.0,
        max_value=15.0,
        value=9.4,
        step=0.1,
        help="Alcohol percentage by volume"
    )

st.markdown("---")

# Predict button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    predict_button = st.button("🔮 Predict Wine Quality", use_container_width=True)

if predict_button:
    # Prepare data
    data = {
        "fixed_acidity": float(fixed_acidity),
        "volatile_acidity": float(volatile_acidity),
        "citric_acid": float(citric_acid),
        "residual_sugar": float(residual_sugar),
        "chlorides": float(chlorides),
        "free_sulfur_dioxide": float(free_sulfur_dioxide),
        "total_sulfur_dioxide": float(total_sulfur_dioxide),
        "density": float(density),
        "pH": float(pH),
        "sulphates": float(sulphates),
        "alcohol": float(alcohol),
        "wine_type_encoded": int(wine_type_encoded)
    }

    # Make prediction
    with st.spinner("Analyzing wine properties..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/predict", json=data)

            if response.status_code == 200:
                result = response.json()
                score = result.get("wine_quality_score", result.get("prediction", 0))
                quality_rating = result.get("quality_rating", "Unknown")

                st.markdown("---")
                st.subheader("📊 Prediction Results")

                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=score,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Wine Quality Score", 'font': {'size': 24}},
                    delta={'reference': 6.0, 'increasing': {'color': "green"}},
                    gauge={
                        'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkred"},
                        'bar': {'color': "#8B0000"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 5], 'color': '#ffcccc'},
                            {'range': [5, 6], 'color': '#ffffcc'},
                            {'range': [6, 7], 'color': '#ccffcc'},
                            {'range': [7, 10], 'color': '#90EE90'}
                        ],
                        'threshold': {
                            'line': {'color': "green", 'width': 4},
                            'thickness': 0.75,
                            'value': 7.0
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
                    if quality_rating == "Excellent":
                        st.success(f"🌟 **{quality_rating}** - Score: {score:.2f}/10")
                        st.info("This is a premium quality wine!")
                    elif quality_rating == "Good":
                        st.success(f"✅ **{quality_rating}** - Score: {score:.2f}/10")
                        st.info("This is a good quality wine.")
                    elif quality_rating == "Average":
                        st.warning(f"😐 **{quality_rating}** - Score: {score:.2f}/10")
                        st.info("This is an average quality wine.")
                    else:
                        st.error(f"❌ **{quality_rating}** - Score: {score:.2f}/10")
                        st.info("This wine may need improvement.")

                # Show detailed results
                st.markdown("### 📋 Detailed Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Quality Score", f"{score:.2f}/10")
                with col2:
                    st.metric("Quality Rating", quality_rating)
                with col3:
                    st.metric("Wine Type", wine_type)

            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.info("Make sure the FastAPI server is running: ./run_api.sh")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray;'>
        <p>Wine Quality Prediction System</p>
        <p>Powered by MLOps Pipeline (ZenML + MLflow + FastAPI)</p>
        <p>Dataset: UCI Wine Quality Dataset</p>
    </div>
""", unsafe_allow_html=True)
