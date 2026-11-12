
import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
from pathlib import Path


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DeSense | Executive Overview",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(120deg, #eaf5ff, #e8f8f5);
    padding: 42px 38px;
    border-radius: 20px;
    border: 1px solid #d8e9f2;
    margin-bottom: 28px;
}

.hero-tag {
    color: #1677a8;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: #123b55;
    font-size: 65px;
    font-weight: 850;
    margin: 5px 0;
    line-height: 1.1;
}

.hero-slogan {
    color: #287b91;
    font-size: 21px;
    font-weight: 600;
    margin-top: 12px;
}

.hero-description {
    color: #496575;
    font-size: 15px;
    line-height: 1.7;
    max-width: 800px;
    margin-top: 12px;
}

.section-title {
    color: #164b68;
    font-size: 23px;
    font-weight: 750;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Apply the clickable effect ONLY to the four KPI buttons */
.st-key-kpi_section div[data-testid="stButton"] button {
    width: 100%;
    min-height: 105px;
    border: 1px solid #dce9ef;
    border-radius: 14px;
    background: #ffffff;
    color: #164b68;
    font-size: 15px;
    font-weight: 700;
    white-space: pre-wrap;
    transition: transform 0.2s ease, box-shadow 0.2s ease,
                background 0.2s ease, border-color 0.2s ease;
    cursor: pointer;
}

.st-key-kpi_section div[data-testid="stButton"] button:hover {
    border-color: #2995a8;
    color: #1677a8;
    background: #f0f9fc;
    transform: translateY(-4px);
    box-shadow: 0 7px 18px rgba(30, 90, 120, 0.14);
}

.st-key-kpi_section div[data-testid="stButton"] button:active {
    transform: scale(0.97);
    box-shadow: 0 2px 6px rgba(30, 90, 120, 0.10);
}

.st-key-kpi_section div[data-testid="stButton"] button:focus-visible {
    outline: 2px solid #2995a8;
    outline-offset: 3px;
}

.insight-box {
    background: #eff8fb;
    border-left: 4px solid #2995a8;
    padding: 17px 20px;
    border-radius: 9px;
    margin: 10px 0;
    color: #31566b;
}

.footer {
    text-align: center;
    color: #8195a2;
    font-size: 13px;
    padding: 30px 0 5px 0;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e3edf2;
    padding: 15px;
    border-radius: 12px;
}
</style>

""", unsafe_allow_html=True)



def render_html(html):
    st.html(textwrap.dedent(html).strip())


# =========================================================
# 3. LOAD DATASET
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

possible_files = [
    PROJECT_DIR / "notebooks" / "DeSense_Feature_Engineered_Dataset.csv",
    PROJECT_DIR / "notebooks" / "DeSense_Ride_Sharing_Cleaned_Dataset.csv",
    PROJECT_DIR / "DeSense_Feature_Engineered_Dataset.csv",
    PROJECT_DIR / "DeSense_Ride_Sharing_Cleaned_Dataset.csv"
]

DATA_PATH = next(
    (p for p in possible_files if p.exists()),
    None
)


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


if DATA_PATH is None:
    st.error("Dataset not found. Check your notebooks folder.")
    st.stop()

try:
    df = load_data(str(DATA_PATH))
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()


# =========================================================
# 4. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Ride_Date",
    "City",
    "Vehicle_Type",
    "Ride_Status",
    "Fare_Amount",
    "Ride_Distance_km"
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()


# =========================================================
# 5. DATA PREPARATION
# =========================================================

df["Ride_Date"] = pd.to_datetime(
    df["Ride_Date"], errors="coerce"
)

df["Fare_Amount"] = pd.to_numeric(
    df["Fare_Amount"], errors="coerce"
)

df["Ride_Distance_km"] = pd.to_numeric(
    df["Ride_Distance_km"], errors="coerce"
)

df = df.dropna(subset=["Ride_Date"]).copy()

for col in ["City", "Vehicle_Type", "Ride_Status"]:
    df[col] = (
        df[col].fillna("Unknown").astype(str).str.strip()
    )

df["Status_Normalized"] = df["Ride_Status"].str.lower()

df["Month"] = df["Ride_Date"].dt.to_period("M").astype(str)


# =========================================================
# 6. HERO SECTION
# =========================================================

render_html("""
<div class="hero">
    <div class="hero-tag">RIDE SHARING ANALYTICS</div>

    <div class="hero-title">DeSense</div>

    <div class="hero-slogan">
        Turning Ride Data into Meaningful Mobility Insights.
    </div>

    <div class="hero-description">
        Explore overall ride performance, monitor revenue trends,
        discover business opportunities and understand mobility
        patterns through data-driven insights.
    </div>
</div>
""")


# =========================================================
# 7. SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.caption("Customize your overview")

min_date = df["Ride_Date"].min().date()
max_date = df["Ride_Date"].max().date()

date_selection = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_selection, (tuple, list)):
    if len(date_selection) == 2:
        start_date, end_date = date_selection
    elif len(date_selection) == 1:
        start_date = end_date = date_selection[0]
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = end_date = date_selection


cities = sorted(df["City"].unique())

selected_cities = st.sidebar.multiselect(
    "Select City",
    cities,
    default=cities
)

vehicles = sorted(df["Vehicle_Type"].unique())

selected_vehicles = st.sidebar.multiselect(
    "Select Vehicle Type",
    vehicles,
    default=vehicles
)


# =========================================================
# 8. APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Ride_Date"].dt.date >= start_date) &
    (df["Ride_Date"].dt.date <= end_date) &
    (df["City"].isin(selected_cities)) &
    (df["Vehicle_Type"].isin(selected_vehicles))
].copy()

if filtered_df.empty:
    st.warning("No records found. Please change your filters.")
    st.stop()


# =========================================================
# 9. KPI CALCULATIONS
# =========================================================

completed_df = filtered_df[
    filtered_df["Status_Normalized"] == "completed"
].copy()

total_rides = len(filtered_df)

total_revenue = completed_df["Fare_Amount"].sum()

average_fare = completed_df["Fare_Amount"].mean()

average_distance = filtered_df["Ride_Distance_km"].mean()

completed_rides = len(completed_df)

completion_rate = (
    completed_rides / total_rides * 100
    if total_rides else 0
)

average_fare = (
    average_fare if pd.notna(average_fare) else 0
)

average_distance = (
    average_distance if pd.notna(average_distance) else 0
)


# =========================================================
# 10. INTERACTIVE KPI CARDS
# =========================================================

render_html("""
<div class="section-title">
    📌 Key Performance Indicators
</div>
""")

st.caption("Select a KPI card to explore its key information.")

if "selected_kpi" not in st.session_state:
    st.session_state["selected_kpi"] = "rides"

with st.container(key="kpi_section"):
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        if st.button(
            f"🚕 TOTAL RIDES\n{total_rides:,}",
            key="kpi_rides",
            use_container_width=True
        ):
            st.session_state["selected_kpi"] = "rides"

    with k2:
        if st.button(
            f"💰 TOTAL REVENUE\n₹{total_revenue:,.2f}",
            key="kpi_revenue",
            use_container_width=True
        ):
            st.session_state["selected_kpi"] = "revenue"

    with k3:
        if st.button(
            f"📊 AVERAGE FARE\n₹{average_fare:,.2f}",
            key="kpi_fare",
            use_container_width=True
        ):
            st.session_state["selected_kpi"] = "fare"

    with k4:
        if st.button(
            f"📍 AVG. DISTANCE\n{average_distance:.2f} km",
            key="kpi_distance",
            use_container_width=True
        ):
            st.session_state["selected_kpi"] = "distance"


# =========================================================
# 11. KPI INTERACTION PANEL
# =========================================================

selected_kpi = st.session_state["selected_kpi"]

if selected_kpi == "rides":
    st.info(
        f"🚕 Your selected dataset contains {total_rides:,} rides "
        f"within the current filters."
    )

elif selected_kpi == "revenue":
    st.info(
        f"💰 Completed rides generated ₹{total_revenue:,.2f} "
        "in total revenue."
    )

elif selected_kpi == "fare":
    st.info(
        f"📊 The average fare of completed rides is "
        f"₹{average_fare:,.2f}."
    )

elif selected_kpi == "distance":
    st.info(
        f"📍 The average ride distance is "
        f"{average_distance:.2f} km."
    )


# =========================================================
# 12. MONTHLY RIDE PERFORMANCE
# =========================================================

st.markdown("---")

render_html("""
<div class="section-title">
    📈 Monthly Ride Performance
</div>
""")

st.caption(
    "Track the overall number of rides across different months."
)

monthly_rides = (
    filtered_df.groupby("Month")
    .size()
    .reset_index(name="Total Rides")
    .sort_values("Month")
)

fig_rides = px.line(
    monthly_rides,
    x="Month",
    y="Total Rides",
    markers=True,
    template="plotly_white",
    title="Monthly Ride Volume",
    labels={
        "Month": "Month",
        "Total Rides": "Number of Rides"
    }
)

fig_rides.update_traces(
    line=dict(color="#168aad", width=3),
    marker=dict(size=8)
)

fig_rides.update_layout(
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Total Rides"
)

st.plotly_chart(
    fig_rides,
    use_container_width=True
)


# =========================================================
# 13. MONTHLY REVENUE PERFORMANCE
# =========================================================

render_html("""
<div class="section-title">
    💰 Monthly Revenue Performance
</div>
""")

st.caption(
    "Understand how revenue changes over time through completed rides."
)

if not completed_df.empty:

    monthly_revenue = (
        completed_df.groupby("Month")["Fare_Amount"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    fig_revenue = px.area(
        monthly_revenue,
        x="Month",
        y="Fare_Amount",
        template="plotly_white",
        title="Monthly Revenue Trend",
        labels={
            "Month": "Month",
            "Fare_Amount": "Revenue (₹)"
        }
    )

    fig_revenue.update_traces(
        line=dict(color="#159a9c", width=3),
        fillcolor="rgba(21,154,156,0.18)"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True
    )

else:
    st.info("No completed rides are available for revenue analysis.")


# =========================================================
# 14. TOP FIVE CITIES
# =========================================================

st.markdown("---")

render_html("""
<div class="section-title">
    🏙️ Top Performing Cities
</div>
""")

st.caption(
    "Cities ranked by ride volume in the selected period."
)

city_summary = (
    filtered_df.groupby("City")
    .agg(
        Total_Rides=("City", "size"),
        Total_Revenue=("Fare_Amount", "sum")
    )
    .reset_index()
)

city_summary["Average_Revenue_Per_Ride"] = (
    city_summary["Total_Revenue"] /
    city_summary["Total_Rides"]
)

city_summary = (
    city_summary.sort_values(
        "Total_Rides", ascending=False
    ).head(5).reset_index(drop=True)
)

city_summary.index = city_summary.index + 1

city_summary = city_summary.rename(columns={
    "Total_Rides": "Total Rides",
    "Total_Revenue": "Total Fare Amount (₹)",
    "Average_Revenue_Per_Ride": "Avg. Fare per Ride (₹)"
})

st.dataframe(
    city_summary.style.format({
        "Total Fare Amount (₹)": "₹{:,.2f}",
        "Avg. Fare per Ride (₹)": "₹{:,.2f}"
    }),
    use_container_width=True
)


# =========================================================
# 15. AUTOMATIC BUSINESS INSIGHTS
# =========================================================

st.markdown("---")

render_html("""
<div class="section-title">
    💡 Business Insights
</div>
""")

insight_col1, insight_col2 = st.columns(2)

top_city = filtered_df["City"].value_counts().idxmax()

top_vehicle = (
    filtered_df["Vehicle_Type"].value_counts().idxmax()
)

with insight_col1:
    st.info(
        f"🏙️ **Most Active City: {top_city}**\n\n"
        "This city has the highest number of rides "
        "in the selected period."
    )

with insight_col2:
    st.info(
        f"🚘 **Most Popular Vehicle: {top_vehicle}**\n\n"
        "This vehicle type accounts for the highest "
        "number of rides in the selected data."
    )

if not completed_df.empty:

    top_revenue_city = (
        completed_df.groupby("City")["Fare_Amount"]
        .sum()
        .idxmax()
    )

    st.success(
        f"💰 **Highest Revenue City:** {top_revenue_city}"
    )

st.metric(
    "Ride Completion Rate",
    f"{completion_rate:.2f}%"
)


# =========================================================
# 16. RECENT RIDE RECORDS
# =========================================================

st.markdown("---")

render_html("""
<div class="section-title">
    🕒 Recent Ride Records
</div>
""")

recent_columns = [
    col for col in [
        "Ride_ID",
        "Ride_Date",
        "City",
        "Vehicle_Type",
        "Ride_Status",
        "Ride_Distance_km",
        "Fare_Amount"
    ]
    if col in filtered_df.columns
]

recent_rides = (
    filtered_df.sort_values(
        "Ride_Date", ascending=False
    )[recent_columns].head(10).copy()
)

st.dataframe(
    recent_rides,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 17. DOWNLOAD FILTERED DATA
# =========================================================

st.markdown("---")

render_html("""
<div class="section-title">
    ⬇️ Export Dashboard Data
</div>
""")

csv_data = (
    filtered_df.drop(
        columns=["Status_Normalized", "Month"],
        errors="ignore"
    )
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Filtered Dataset (CSV)",
    data=csv_data,
    file_name="DeSense_Filtered_Ride_Data.csv",
    mime="text/csv"
)


# =========================================================
# 18. FOOTER
# =========================================================

st.markdown(
    """
    <div style="text-align:center; color:#8A9AA5; font-size:12px;
                padding:18px 0; border-top:1px solid #E5EDF1; margin-top:40px;">
        © 2026 DeSense | Developed by Sahil | GNDEC Ludhiana
    </div>
    """,
    unsafe_allow_html=True
)
