
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer | DeSense", page_icon="🔍", layout="wide")

st.markdown("""
<style>
.stApp {background:#F5F7FB;}
div[data-testid="stMetric"] {
    background:white;padding:15px;border-radius:12px;
    border:1px solid #E5EAF2;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "notebooks" / "DeSense_Ride_Sharing_Cleaned_Dataset.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()

st.title("🔍 Data Explorer")
st.caption("Search, inspect and understand your ride-sharing dataset.")

# Dataset overview
a, b, c, d = st.columns(4)
a.metric("Total Records", f"{len(df):,}")
b.metric("Total Columns", len(df.columns))
c.metric("Unique Cities", df["City"].nunique())
d.metric("Missing Values", f"{df.isna().sum().sum():,}")

st.divider()

st.subheader("🔎 Search and Filter")

search = st.text_input("Search by Ride ID", placeholder="Enter ride ID")

cities = ["All Cities"] + sorted(df["City"].dropna().unique().tolist())
vehicles = ["All Vehicles"] + sorted(df["Vehicle_Type"].dropna().unique().tolist())
statuses = ["All Statuses"] + sorted(df["Ride_Status"].dropna().unique().tolist())

c1, c2, c3 = st.columns(3)

with c1:
    city = st.selectbox("City", cities)

with c2:
    vehicle = st.selectbox("Vehicle Type", vehicles)

with c3:
    status = st.selectbox("Ride Status", statuses)

filtered = df.copy()

if search.strip() and "Ride_ID" in filtered.columns:
    filtered = filtered[
        filtered["Ride_ID"].astype(str).str.contains(search.strip(), case=False, na=False)
    ]

if city != "All Cities":
    filtered = filtered[filtered["City"] == city]

if vehicle != "All Vehicles":
    filtered = filtered[filtered["Vehicle_Type"] == vehicle]

if status != "All Statuses":
    filtered = filtered[filtered["Ride_Status"] == status]

st.divider()
st.subheader("Filtered Dataset")

x, y = st.columns(2)
x.metric("Matching Records", f"{len(filtered):,}")
y.metric("Columns", len(filtered.columns))

st.dataframe(filtered, use_container_width=True, height=420)

st.download_button(
    "⬇️ Download Filtered CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    "DeSense_Filtered_Dataset.csv",
    "text/csv"
)



st.divider()
st.subheader("📚 Column Information")

info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str).values,
    "Missing Values": df.isna().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(info, use_container_width=True)

with st.expander("View descriptive statistics"):
    st.dataframe(df.describe(include="all").T, use_container_width=True)
st.markdown(
    """
    <div style="text-align:center; color:#8A9AA5; font-size:12px;
                padding:18px 0; border-top:1px solid #E5EDF1; margin-top:40px;">
        © 2026 DeSense | Developed by Sahil | GNDEC Ludhiana
    </div>
    """,
    unsafe_allow_html=True
)