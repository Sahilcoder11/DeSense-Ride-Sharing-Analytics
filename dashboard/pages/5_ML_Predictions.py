
from pathlib import Path
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Fare Prediction | DeSense", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp {background:#F5F7FB;}
div[data-testid="stMetric"] {
    background:white;padding:20px;border-radius:14px;
    border:1px solid #E5EAF2;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "notebooks" / "DeSense_Feature_Engineered_Dataset.csv"
MODEL = ROOT / "dashboard" / "fare_prediction_model.pkl"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

@st.cache_resource
def load_model():
    return joblib.load(MODEL)

st.title("🤖 Ride Fare Prediction")
st.caption("Predict estimated ride fares using Machine Learning.")

if not DATA.exists():
    st.error("Feature-engineered dataset not found.")
    st.stop()

if not MODEL.exists():
    st.error("Trained model file not found.")
    st.stop()

df = load_data()
model = load_model()

st.info(
    "Enter your ride details below. DeSense will estimate "
    "the fare using its trained Random Forest model."
)

st.subheader("🚕 Enter Ride Details")

c1, c2 = st.columns(2)

with c1:
    distance = st.number_input(
        "Ride Distance (km)",
        min_value=0.1,
        max_value=500.0,
        value=10.0,
        step=0.5
    )

    vehicle = st.selectbox(
        "Vehicle Type",
        sorted(df["Vehicle_Type"].dropna().unique())
    )

with c2:
    city = st.selectbox(
        "City",
        sorted(df["City"].dropna().unique())
    )

    surge = st.number_input(
        "Surge Multiplier",
        min_value=0.1,
        max_value=10.0,
        value=1.0,
        step=0.1
    )

st.divider()

if st.button("🔮 Predict Ride Fare", type="primary", use_container_width=True):

    new_ride = pd.DataFrame({
        "Ride_Distance_km": [distance],
        "Vehicle_Type": [vehicle],
        "City": [city],
        "Surge_Multiplier": [surge]
    })

    try:
        prediction = float(model.predict(new_ride)[0])

        st.success("Fare prediction completed!")

        st.metric(
            "Estimated Ride Fare",
            f"₹{max(0, prediction):,.2f}"
        )

        st.caption(
            "This is a model-generated estimate, not a guaranteed actual fare."
        )

        st.subheader("Prediction Summary")

        a, b, c = st.columns(3)
        a.metric("Distance", f"{distance:.2f} km")
        b.metric("Vehicle", vehicle)
        c.metric("Surge", f"{surge:.1f}x")

    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.warning(
            "Check that the model was trained using the same input "
            "columns and preprocessing as this prediction form."
        )

st.divider()

st.subheader("🧠 About the Prediction Model")

st.write("""
DeSense uses a Random Forest Regression model to estimate ride fares.

**Model input features:**
- Ride Distance
- Vehicle Type
- City
- Surge Multiplier

The model was trained using the feature-engineered ride-sharing dataset.
""")
st.markdown(
    """
    <div style="text-align:center; color:#8A9AA5; font-size:12px;
                padding:18px 0; border-top:1px solid #E5EDF1; margin-top:40px;">
        © 2026 DeSense | Developed by Sahil | GNDEC Ludhiana
    </div>
    """,
    unsafe_allow_html=True
)
