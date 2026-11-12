
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ride Analytics | DeSense", page_icon="🚕", layout="wide")

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

st.title("🚕 Ride Analytics")
st.caption("Understand ride demand, city performance and vehicle utilization.")

# Filters
st.sidebar.header("Ride Filters")

cities = sorted(df["City"].dropna().unique())
vehicles = sorted(df["Vehicle_Type"].dropna().unique())
statuses = sorted(df["Ride_Status"].dropna().unique())

selected_cities = st.sidebar.multiselect("Cities", cities, default=cities)
selected_vehicles = st.sidebar.multiselect("Vehicle types", vehicles, default=vehicles)
selected_status = st.sidebar.multiselect("Ride status", statuses, default=statuses)

valid_dates = df["Ride_Date"].dropna()
if not valid_dates.empty:
    date_range = st.sidebar.date_input(
        "Date range",
        (valid_dates.min().date(), valid_dates.max().date())
    )
else:
    date_range = ()

filtered = df[
    df["City"].isin(selected_cities)
    & df["Vehicle_Type"].isin(selected_vehicles)
    & df["Ride_Status"].isin(selected_status)
].copy()

if len(date_range) == 2:
    filtered = filtered[
        filtered["Ride_Date"].dt.date.between(date_range[0], date_range[1])
    ]

if filtered.empty:
    st.warning("No rides match the selected filters.")
    st.stop()

# KPIs
st.subheader("Ride Performance")
a, b, c, d = st.columns(4)
a.metric("Total Rides", f"{len(filtered):,}")
b.metric("Cities", filtered["City"].nunique())
c.metric("Vehicle Types", filtered["Vehicle_Type"].nunique())
d.metric("Average Distance", f"{filtered['Ride_Distance_km'].mean():.2f} km")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    city_data = filtered["City"].value_counts().reset_index()
    city_data.columns = ["City", "Rides"]
    fig = px.bar(city_data.head(10), x="Rides", y="City",
                 orientation="h", title="Top 10 Cities by Rides",
                 color="Rides", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

with right:
    vehicle_data = filtered["Vehicle_Type"].value_counts().reset_index()
    vehicle_data.columns = ["Vehicle", "Rides"]
    fig = px.pie(vehicle_data, names="Vehicle", values="Rides",
                 hole=0.55, title="Vehicle Usage Distribution")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    monthly = (filtered.dropna(subset=["Ride_Date"])
               .assign(Month=lambda x: x["Ride_Date"].dt.to_period("M").astype(str))
               .groupby("Month").size().reset_index(name="Rides"))
    fig = px.line(monthly, x="Month", y="Rides", markers=True,
                  title="Monthly Ride Demand",
                  color_discrete_sequence=["#2563EB"])
    st.plotly_chart(fig, use_container_width=True)

with right:
    distance = filtered.groupby("Vehicle_Type")["Ride_Distance_km"].mean().reset_index()
    fig = px.bar(distance, x="Vehicle_Type", y="Ride_Distance_km",
                 title="Average Distance by Vehicle",
                 color="Ride_Distance_km", color_continuous_scale="Teal")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("💡 Ride Insights")

best_city = filtered["City"].value_counts().idxmax()
best_vehicle = filtered["Vehicle_Type"].value_counts().idxmax()

x, y = st.columns(2)
x.success(f"🏙️ Highest ride volume: **{best_city}**")
y.info(f"🚘 Most used vehicle: **{best_vehicle}**")

with st.expander("View filtered ride records"):
    st.dataframe(filtered, use_container_width=True)
    st.download_button(
        "Download ride data",
        filtered.to_csv(index=False).encode("utf-8"),
        "DeSense_Ride_Analytics.csv",
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