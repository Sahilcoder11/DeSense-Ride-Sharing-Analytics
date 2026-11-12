
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fare Analytics | DeSense", page_icon="💰", layout="wide")

st.markdown("""
<style>
.stApp {background:#F5F7FB;}
.block-container {padding-top:2rem;}
div[data-testid="stMetric"] {
    background:white;padding:15px;border-radius:12px;
    border:1px solid #E5EAF2;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "notebooks" / "DeSense_Feature_Engineered_Dataset.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    df["Ride_Date"] = pd.to_datetime(df["Ride_Date"], errors="coerce")
    df["Ride_Status"] = df["Ride_Status"].astype("string").str.strip().str.title()
    return df

df = load_data()
st.title("💰 Fare Analytics")
st.caption("Explore revenue patterns, fare distribution and pricing behaviour.")

st.sidebar.header("Fare Filters")

cities = ["All Cities"] + sorted(df["City"].dropna().unique().tolist())
vehicles = ["All Vehicles"] + sorted(df["Vehicle_Type"].dropna().unique().tolist())

city = st.sidebar.selectbox("City", cities)
vehicle = st.sidebar.selectbox("Vehicle", vehicles)

filtered = df.copy()

if city != "All Cities":
    filtered = filtered[filtered["City"] == city]

if vehicle != "All Vehicles":
    filtered = filtered[filtered["Vehicle_Type"] == vehicle]

# Revenue calculations use completed rides only
completed = filtered[
    filtered["Ride_Status"].str.lower() == "completed"
].copy()

if completed.empty:
    st.warning("No completed rides found for these filters.")
    st.stop()

revenue = completed["Fare_Amount"].sum()
avg_fare = completed["Fare_Amount"].mean()
median_fare = completed["Fare_Amount"].median()
total_rides = len(completed)

st.subheader("Revenue Overview")
a, b, c, d = st.columns(4)
a.metric("Total Revenue", f"₹{revenue:,.0f}")
b.metric("Completed Rides", f"{total_rides:,}")
c.metric("Average Fare", f"₹{avg_fare:,.2f}")
d.metric("Median Fare", f"₹{median_fare:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    city_revenue = completed.groupby("City")["Fare_Amount"].sum().nlargest(10).reset_index()
    fig = px.bar(city_revenue, x="Fare_Amount", y="City", orientation="h",
                 title="Top Cities by Revenue",
                 color="Fare_Amount", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.histogram(completed, x="Fare_Amount", nbins=30,
                       title="Fare Distribution",
                       color_discrete_sequence=["#0D9488"])
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    vehicle_fare = completed.groupby("Vehicle_Type")["Fare_Amount"].mean().reset_index()
    fig = px.bar(vehicle_fare, x="Vehicle_Type", y="Fare_Amount",
                 title="Average Fare by Vehicle",
                 color="Fare_Amount", color_continuous_scale="Teal")
    st.plotly_chart(fig, use_container_width=True)

with right:
    if "Payment_Method" in completed.columns:
        payment = completed.groupby("Payment_Method")["Fare_Amount"].sum().reset_index()
        fig = px.pie(payment, names="Payment_Method", values="Fare_Amount",
                     hole=0.5, title="Revenue by Payment Method")
        st.plotly_chart(fig, use_container_width=True)

if "Surge_Multiplier" in completed.columns:
    st.divider()
    surge = completed.groupby("Surge_Multiplier")["Fare_Amount"].mean().reset_index()
    fig = px.line(surge, x="Surge_Multiplier", y="Fare_Amount",
                  markers=True, title="Average Fare by Surge Multiplier")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📋 Completed Ride Fare Records")
st.dataframe(completed, use_container_width=True)

st.download_button(
    "⬇️ Download fare data",
    completed.to_csv(index=False).encode("utf-8"),
    "DeSense_Fare_Analytics.csv",
    "text/csv"
)
st.markdown(
    """
    <div style="text-align:center; color:#8A9AA5; font-size:12px;
                padding:18px 0; border-top:1px solid #E5EDF1; margin-top:40px;">
        © 2026 DeSense | Developed by Sahil | GNDEC Ludhiana
    </div>
    """,
    unsafe_allow_html=True
)