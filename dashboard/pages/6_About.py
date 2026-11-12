import streamlit as st
import textwrap

st.set_page_config(
    page_title="About DeSense",
    page_icon="🚕",
    layout="wide"
)

# -------------------- STYLING --------------------

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.about-hero {
    background: linear-gradient(120deg, #eaf5ff, #e8f8f5);
    padding: 34px;
    border-radius: 18px;
    border: 1px solid #d8e9f2;
    margin-bottom: 24px;
}

.about-tag {
    color: #1677a8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.about-title {
    color: #123b55;
    font-size: 44px;
    font-weight: 800;
    margin: 8px 0;
}

.about-subtitle {
    color: #287b91;
    font-size: 19px;
    font-weight: 600;
}

.about-description {
    color: #496575;
    font-size: 15px;
    line-height: 1.7;
    max-width: 850px;
    margin-top: 12px;
}

.section-heading {
    color: #164b68;
    font-size: 22px;
    font-weight: 750;
    margin: 24px 0 12px 0;
}

.info-card {
    background: white;
    border: 1px solid #e1eaf0;
    border-radius: 13px;
    padding: 18px;
    min-height: 135px;
    margin-bottom: 12px;
    transition: 0.2s ease;
}

.info-card:hover {
    border-color: #64b5c5;
    transform: translateY(-3px);
    box-shadow: 0 5px 16px rgba(30, 90, 120, 0.08);
}

.info-card h4 {
    color: #176b83;
    margin: 0 0 8px 0;
}

.info-card p {
    color: #587080;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.workflow-item {
    background: #f3f8fb;
    border-left: 4px solid #2995a8;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 9px;
    color: #607987;
    font-size: 14px;
}

.developer-card {
    background: linear-gradient(120deg, #f0f7fc, #effaf8);
    border: 1px solid #dcebf0;
    padding: 22px;
    border-radius: 14px;
    color: #31566b;
    line-height: 1.9;
}

.footer-text {
    text-align: center;
    color: #8195a2;
    font-size: 13px;
    padding: 24px 0 5px;
}
</style>
""", unsafe_allow_html=True)


def render_html(content):
    st.html(textwrap.dedent(content).strip())


# -------------------- HERO --------------------

render_html("""
<div class="about-hero">
    <div class="about-tag">ABOUT THE PROJECT</div>
    <div class="about-title">DeSense</div>
    <div class="about-subtitle">Ride Sharing Analytics Dashboard</div>
    <div class="about-description">
        Turning ride-sharing data into meaningful mobility insights.
        DeSense is an interactive analytics platform for exploring ride
        patterns, understanding fare trends and demonstrating
        machine-learning-based fare prediction.
    </div>
</div>
""")


# -------------------- OVERVIEW --------------------

st.markdown('<div class="section-heading">📌 Project Overview</div>',
            unsafe_allow_html=True)

st.write(
    "DeSense analyses ride-sharing data to understand ride demand, "
    "distance, vehicle usage and fare patterns. The project follows a "
    "data science workflow involving data exploration, quality "
    "assessment, cleaning, feature engineering, visualization and "
    "machine learning. The results are presented through an interactive "
    "Streamlit dashboard."
)


# -------------------- KEY FEATURES --------------------

st.markdown('<div class="section-heading">✨ What DeSense Offers</div>',
            unsafe_allow_html=True)

features = [
    (
        "📊 Data Analytics",
        "Explore ride activity, city trends, vehicle usage and fare patterns."
    ),
    (
        "📈 Interactive Dashboard",
        "Use filters and interactive visualizations to discover insights."
    ),
    (
        "🤖 Fare Prediction",
        "Estimate ride fares using a trained Random Forest model."
    )
]

cols = st.columns(3)
for col, (title, description) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="info-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)


# -------------------- WORKFLOW --------------------

st.markdown('<div class="section-heading">⚙️ Project Workflow</div>',
            unsafe_allow_html=True)

workflow = [
    "01  Data Exploration — understand dataset structure and distributions.",
    "02  Data Quality — identify missing values, duplicates and inconsistencies.",
    "03  Data Cleaning — prepare the dataset for reliable analysis.",
    "04  Feature Engineering — create useful features for analysis and modelling.",
    "05  Visualization — explore trends through interactive charts.",
    "06  Machine Learning & Dashboard — train the fare model and present results in Streamlit."
]

for item in workflow:
    st.markdown(
        f'<div class="workflow-item">{item}</div>',
        unsafe_allow_html=True
    )


# -------------------- TECHNOLOGY STACK --------------------

st.markdown(
    '<div class="section-heading">💻 Technologies & Tools</div>',
    unsafe_allow_html=True
)

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.markdown("""
    <div class="info-card">
        <h4>🐍 Python</h4>
        <p>Core programming language used for data processing,
        analysis and machine learning.</p>
    </div>
    """, unsafe_allow_html=True)

with tech2:
    st.markdown("""
    <div class="info-card">
        <h4>🐼 Pandas & NumPy</h4>
        <p>Used for dataset manipulation, numerical operations,
        cleaning and feature engineering.</p>
    </div>
    """, unsafe_allow_html=True)

with tech3:
    st.markdown("""
    <div class="info-card">
        <h4>📊 Plotly</h4>
        <p>Used to create interactive charts and visual
        representations of ride-sharing data.</p>
    </div>
    """, unsafe_allow_html=True)

tech4, tech5, tech6 = st.columns(3)

with tech4:
    st.markdown("""
    <div class="info-card">
        <h4>🌐 Streamlit</h4>
        <p>Used to develop the interactive web-based
        analytics dashboard.</p>
    </div>
    """, unsafe_allow_html=True)

with tech5:
    st.markdown("""
    <div class="info-card">
        <h4>🤖 Scikit-learn</h4>
        <p>Used for machine learning model development
        and fare prediction.</p>
    </div>
    """, unsafe_allow_html=True)

with tech6:
    st.markdown("""
    <div class="info-card">
        <h4>💡 VS Code & Jupyter</h4>
        <p>Development environments used for coding,
        experimentation and notebook-based analysis.</p>
    </div>
    """, unsafe_allow_html=True)



# -------------------- DEVELOPER --------------------

st.markdown('<div class="section-heading">👨‍💻 Developer Information</div>',
            unsafe_allow_html=True)

st.markdown("""
<div class="developer-card">
    <b>Developed By:</b> Sahil<br>
    <b>Programme:</b> B.Tech – Computer Science and Engineering<br>
    <b>Institution:</b> Guru Nanak Dev Engineering College, Ludhiana<br>
    <b>Project Domain:</b> Data Science and Analytics<br>
    <b>Project Title:</b> DeSense – Ride Sharing Analytics Dashboard
</div>
""", unsafe_allow_html=True)


# -------------------- FOOTER --------------------

st.markdown(
    """
    <div style="text-align:center; color:#8A9AA5; font-size:12px;
                padding:18px 0; border-top:1px solid #E5EDF1; margin-top:40px;">
        © 2026 DeSense | Developed by Sahil | GNDEC Ludhiana
    </div>
    """,
    unsafe_allow_html=True
)
