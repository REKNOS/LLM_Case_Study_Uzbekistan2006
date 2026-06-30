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

    st.plotly_chart(fig_theme, width="stretch")

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

    st.plotly_chart(fig_eval, width="stretch")

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

    st.plotly_chart(fig_hdi, width="stretch")

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

    st.plotly_chart(fig_life, width="stretch")


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

st.plotly_chart(fig_gdi, width="stretch")

# ==========================================================
# PART 3 - ADVANCED VISUALISATIONS
# ==========================================================

st.markdown("---")
st.header("📈 Advanced Development Analytics")

# ----------------------------------------------------------
# HDI Gauge Chart
# ----------------------------------------------------------

col1, col2 = st.columns([1, 2])

with col1:

    st.subheader("🌍 HDI Score")

    hdi_value = float(indicator_dict.get("HDI", 0))

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=hdi_value,
        title={'text': "Human Development Index"},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 0.55], 'color': "#ffcccc"},
                {'range': [0.55, 0.70], 'color': "#ffe680"},
                {'range': [0.70, 0.80], 'color': "#b3ffb3"},
                {'range': [0.80, 1.00], 'color': "#66ff99"}
            ]
        }
    ))

    gauge.update_layout(height=350)

    st.plotly_chart(gauge, width="stretch")

# ----------------------------------------------------------
# Radar Chart
# ----------------------------------------------------------

with col2:

    st.subheader("🕸 Development Indicator Radar")

    radar_categories = [
        "HDI",
        "Education",
        "Literacy",
        "Life Expectancy"
    ]

    radar_values = [

        float(indicator_dict.get("HDI",0)),

        float(indicator_dict.get("Education Index",0)),

        float(indicator_dict.get("Literacy Rate",0))/100,

        float(indicator_dict.get("Life Expectancy Index",0))

    ]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(

        r=radar_values,

        theta=radar_categories,

        fill='toself',

        name="Uzbekistan"

    ))

    radar.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0,1]

            )

        ),

        showlegend=False,

        height=450

    )

    st.plotly_chart(radar, width="stretch")

# ==========================================================
# MODEL COMPARISON
# ==========================================================

st.markdown("---")
st.header("🤖 Local LLM Behaviour Comparison")

st.info(
    "This comparison shows the output length generated by each local LLM. "
    "Longer outputs generally indicate more detailed responses, although they "
    "may also contain additional verbosity."
)

fig_compare = px.bar(
    comparison_df,
    x="Model",
    y="Output_Length",
    color="Model",
    text="Output_Length",
    title="LLM Output Length Comparison"
)

fig_compare.update_traces(
    textposition="outside"
)

fig_compare.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Local LLM",
    yaxis_title="Number of Characters",
    showlegend=False
)

st.plotly_chart(fig_compare, width="stretch")

# ==========================================================
# PART 4 - DEVELOPMENT INSIGHTS
# ==========================================================

st.markdown("---")
st.header("📝 Development Insights")

# ----------------------------------------------------------
# Executive Summary
# ----------------------------------------------------------

st.subheader("📄 Executive Summary")

st.info(executive_summary)

st.markdown("---")

# ----------------------------------------------------------
# Strengths & Challenges
# ----------------------------------------------------------

st.subheader("💡 Development Strengths & Challenges")

strength_file = os.path.join(OUTPUT_DIR, "strengths_challenges.json")

if os.path.exists(strength_file):

    with open(strength_file, "r", encoding="utf-8") as f:
        strengths = json.load(f)

    # Support both naming styles
    strength_list = strengths.get(
        "development_strengths",
        strengths.get("developmentStrengths", [])
    )

    challenge_list = strengths.get(
        "development_challenges",
        strengths.get("developmentChallenges", [])
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("### ✅ Development Strengths")

        for item in strength_list:
            st.markdown(f"- {item}")

    with col2:
        st.error("### ⚠ Development Challenges")

        for item in challenge_list:
            st.markdown(f"- {item}")

else:
    st.warning("strengths_challenges.json not found.")
# ----------------------------------------------------------
# Chapter Summaries
# ----------------------------------------------------------

st.subheader("📚 Chapter Summaries")

if len(chapter_summaries) > 0:

    for chapter, summary in chapter_summaries.items():

        with st.expander(chapter):

            st.write(summary)

else:

    st.warning("No chapter summaries available.")

st.markdown("---")

# ----------------------------------------------------------
# LLM Evaluation
# ----------------------------------------------------------

st.subheader("🤖 LLM Evaluation")

evaluation_file = os.path.join(OUTPUT_DIR, "evaluation_scores.csv")

if os.path.exists(evaluation_file):

    eval_df = pd.read_csv(evaluation_file)

    st.dataframe(eval_df, width="stretch")

    avg = round(eval_df["Score"].mean(),2)

    st.metric("Average Evaluation Score", avg)

    if avg >= 4:

        st.success(
            "Overall extraction quality is high. "
            "The evaluator model found the outputs consistent, complete and factually aligned."
        )

    elif avg >= 3:

        st.warning(
            "Overall extraction quality is acceptable but could be improved."
        )

    else:

        st.error(
            "Extraction quality is relatively low and requires prompt refinement."
        )

else:

    st.warning("evaluation_scores.csv not found.")

# ==========================================================
# PART 5 - DOWNLOADS & PROJECT SUMMARY
# ==========================================================

st.markdown("---")

st.header("📂 Download Extracted Outputs")

col1, col2, col3 = st.columns(3)

# -----------------------------
# Theme Distribution CSV
# -----------------------------
with col1:

    csv = theme_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Theme Distribution",
        data=csv,
        file_name="theme_distribution.csv",
        mime="text/csv"
    )

# -----------------------------
# Indicator CSV
# -----------------------------
with col2:

    csv = indicator_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Indicators",
        data=csv,
        file_name="indicator_values.csv",
        mime="text/csv"
    )

# -----------------------------
# Evaluation CSV
# -----------------------------
with col3:

    csv = evaluation_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Evaluation",
        data=csv,
        file_name="evaluation_scores.csv",
        mime="text/csv"
    )

st.markdown("---")

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.header("📑 Extracted Dataset Preview")

tab1, tab2, tab3 = st.tabs([
    "Indicators",
    "Theme Distribution",
    "Model Comparison"
])

with tab1:
    st.dataframe(indicator_df, width="stretch")

with tab2:
    st.dataframe(theme_df, width="stretch")

with tab3:
    st.dataframe(comparison_df, width="stretch")

st.markdown("---")

# ==========================================================
# PROJECT CONCLUSION
# ==========================================================

st.header("📖 Project Conclusion")

st.success("""
This dashboard demonstrates a complete Local LLM pipeline for extracting,
evaluating and visualising information from the Uzbekistan Human Development Report (2006).

The pipeline includes:

• PDF Parsing

• Text Chunking

• Retrieval-Augmented Generation (RAG)

• Local LLM Information Extraction

• LLM-based Evaluation

• Structured JSON Generation

• Interactive Visual Analytics

• Cross-Model Behaviour Comparison

The results indicate that local Large Language Models can effectively transform
large policy documents into structured intelligence suitable for dashboards and
decision support.
""")

st.markdown("---")

# ==========================================================
# TECHNOLOGIES
# ==========================================================

st.header("🛠 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:

    st.info("""
**Framework**

• Ollama

• LangChain

• ChromaDB

• Streamlit
""")

with tech2:

    st.info("""
**Local LLMs**

• Llama 3.2

• Qwen 2.5

• Phi-3 Mini
""")

with tech3:

    st.info("""
**Python Libraries**

• Pandas

• Plotly

• PyMuPDF

• JSON

• Matplotlib
""")

st.markdown("---")

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Human Development Intelligence Dashboard | "
    "University Assignment | "
    "Uzbekistan Human Development Report (2006) | "
    "Developed using Local Large Language Models"
)