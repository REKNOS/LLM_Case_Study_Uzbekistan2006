import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Uzbekistan Human Development Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main{
    background-color:#F7F9FC;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.metric-container{
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

h1,h2,h3{
    color:#0F4C81;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# ==========================================================
# LOAD DATA
# ==========================================================

theme_df = pd.read_csv(os.path.join(OUTPUT_DIR,"theme_distribution.csv"))
indicator_df = pd.read_csv(os.path.join(OUTPUT_DIR,"indicator_values.csv"))
hdi_df = pd.read_csv(os.path.join(OUTPUT_DIR,"hdi_trend.csv"))
life_df = pd.read_csv(os.path.join(OUTPUT_DIR,"life_expectancy.csv"))
gdi_df = pd.read_csv(os.path.join(OUTPUT_DIR,"gdi_trend.csv"))
evaluation_df = pd.read_csv(os.path.join(OUTPUT_DIR,"evaluation_scores.csv"))
comparison_df = pd.read_csv(os.path.join(OUTPUT_DIR,"model_comparison.csv"))

# ==========================================================
# LOAD TEXT FILES
# ==========================================================

def read_file(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        with open(path,"r",encoding="utf-8") as f:
            return f.read()
    return "Not Available"

executive_summary = read_file("executive_summary.txt")
strengths_text = read_file("strengths_challenges.txt")
evaluation_text = read_file("evaluation.txt")

chapter_file = os.path.join(OUTPUT_DIR,"chapter_summaries.json")

if os.path.exists(chapter_file):
    with open(chapter_file,"r",encoding="utf-8") as f:
        chapter_summaries = json.load(f)
else:
    chapter_summaries = {}

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Uzbekistan.svg", width=180)

st.sidebar.title("Project Information")

st.sidebar.markdown("""
### Country
Uzbekistan

### Report
Human Development Report 2006

### Student ID
24141654

### Local Models

✅ Llama 3.2

✅ Qwen 2.5

✅ Phi-3

### Framework

- Ollama
- LangChain
- ChromaDB
- Streamlit
""")

# ==========================================================
# HEADER
# ==========================================================

st.title("🇺🇿 Uzbekistan Human Development Intelligence Dashboard")

st.markdown("""
This dashboard presents information extracted automatically from the **2006 Uzbekistan Human Development Report**
using **Local Large Language Models (LLMs)**.
""")

st.divider()

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📌 Key Development Indicators")

# Convert indicator table to dictionary
indicator_dict = dict(zip(indicator_df.iloc[:,0], indicator_df.iloc[:,1]))

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "HDI",
        indicator_dict.get("HDI","N/A")
    )

with col2:
    st.metric(
        "GDP Per Capita",
        indicator_dict.get("GDP Per Capita", indicator_dict.get("GDP Per Capita (PPP$)", "N/A"))
    )

with col3:
    st.metric(
        "Literacy Rate",
        indicator_dict.get("Literacy Rate","N/A")
    )   

with col4:
    st.metric(
        "Life Expectancy Index",
        indicator_dict.get("Life Expectancy Index","N/A")
    )

st.divider()

st.success("✅ Dashboard loaded successfully.")

# ==========================================================
# THEME DISTRIBUTION & EVALUATION
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Theme Distribution")

    fig_theme = px.bar(
        theme_df,
        x="Theme",
        y="Score",
        color="Score",
        text="Score",
        color_continuous_scale="Viridis"
    )

    fig_theme.update_layout(
        template="plotly_dark",
        height=430,
        xaxis_title="Theme",
        yaxis_title="Score",
        showlegend=False
    )

    st.plotly_chart(fig_theme, use_container_width=True)

with col2:

    st.subheader("🤖 LLM Evaluation Scores")

    fig_eval = px.bar(
        evaluation_df,
        x="Metric",
        y="Score",
        color="Score",
        text="Score",
        color_continuous_scale="Blues"
    )

    fig_eval.update_layout(
        template="plotly_dark",
        height=430,
        showlegend=False
    )

    st.plotly_chart(fig_eval, use_container_width=True)

    # ==========================================================
# HDI & LIFE EXPECTANCY
# ==========================================================

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.subheader("📈 HDI Trend")

    fig_hdi = px.line(
        hdi_df,
        x="Year",
        y="HDI",
        markers=True
    )

    fig_hdi.update_traces(line_width=4)

    fig_hdi.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(fig_hdi, use_container_width=True)

with col4:

    st.subheader("❤️ Life Expectancy Trend")

    fig_life = px.line(
        life_df,
        x="Year",
        y="LifeExpectancy",
        markers=True
    )

    fig_life.update_traces(line_width=4)

    fig_life.update_layout(
        template="plotly_dark",
        height=430
    )

    st.plotly_chart(fig_life, use_container_width=True)


    # ==========================================================
# GDI TREND
# ==========================================================

st.markdown("---")

st.subheader("🌍 Gender Development Index")

fig_gdi = px.line(
    gdi_df,
    x="Year",
    y="GDI",
    markers=True
)

fig_gdi.update_traces(line_width=4)

fig_gdi.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(fig_gdi, use_container_width=True)
