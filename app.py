import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.extractor import extract_text
from utils.preprocessing import extract_experience
from utils.intelligence import (
    auto_detect_industry,
    extract_contact_info,
    get_skills_by_industry,
    analyze_skill_gap
)
from utils.scorer import calculate_final_score, advanced_score
from utils.report_generator import generate_report
from utils.feedback_engine import generate_feedback


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Intelligence Pro",
    page_icon="🎯",
    layout="wide"
)

# ---------------- DARK NAVY CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0F172A;
}

/* Bright White Text */
html, body, [class*="css"]  {
    color: #FFFFFF !important;
}

/* Metrics */
[data-testid="stMetricLabel"] {
    color: #E2E8F0 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #FFFFFF !important;
}

/* Dataframe text */
thead tr th {
    color: #FFFFFF !important;
}

tbody tr td {
    color: #FFFFFF !important;
}

/* Success / Error boxes text */
.stSuccess, .stWarning, .stError {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("## 🚀 AI Resume Intelligence Pro")
st.markdown(
    "<span style='color:#2563EB;font-size:18px;'>Advanced ATS-Level Resume Analysis System</span>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- FILE UPLOAD ----------------
resume_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

analyze_btn = st.button("Generate Advanced Analysis", use_container_width=True)

# ---------------- ANALYSIS ----------------
if analyze_btn:

    if resume_file:

        with st.spinner("Analyzing Resume..."):

            resume_raw = extract_text(resume_file)

            industry = auto_detect_industry(resume_raw)
            contact = extract_contact_info(resume_raw)
            experience_years = extract_experience(resume_raw)

            resume_skills = get_skills_by_industry(resume_raw, industry)
            missing_skills = analyze_skill_gap(resume_skills, industry)

            skill_base_score = min(len(resume_skills) * 8, 100)
            legacy_score, candidate_type = calculate_final_score(
                skill_base_score,
                experience_years
            )

            final_score, breakdown = advanced_score(
                skill_count=len(resume_skills),
                total_possible_skills=30,
                experience_years=experience_years,
                resume_text=resume_raw
            )

            feedback = generate_feedback(
                skill_score=breakdown["Skill Score"],
                experience_years=experience_years,
                missing_skills=missing_skills,
                keyword_density=breakdown["Keyword Density"]
            )

            report_df = generate_report(
                final_score,
                resume_skills,
                missing_skills
            )

        # ---------------- OVERVIEW ----------------
        st.markdown("## 📊 Analysis Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Overall ATS Score", f"{final_score}%")
        col2.metric("Candidate Type", candidate_type)
        col3.metric("Experience (Years)", experience_years)

        st.markdown("---")

        # ---------------- BREAKDOWN ----------------
        st.subheader("🧠 Intelligence Breakdown")

        breakdown_cols = st.columns(len(breakdown))

        for i, key in enumerate(breakdown.keys()):
            breakdown_cols[i].metric(key, breakdown[key])

        st.markdown("---")

        # ---------------- RADAR ----------------
        st.subheader("📈 Radar Analysis")

        categories = list(breakdown.keys())
        values = list(breakdown.values())

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # ---------------- TABS ----------------
        tab1, tab2, tab3, tab4 = st.tabs(
            ["🎯 Skills", "❌ Skill Gaps", "📞 Contact", "📋 Feedback"]
        )

        with tab1:
            if resume_skills:
                cols = st.columns(3)
                for i, skill in enumerate(resume_skills):
                    cols[i % 3].success(skill)
            else:
                st.warning("No skills detected.")

        with tab2:
            if missing_skills:
                cols = st.columns(3)
                for i, skill in enumerate(missing_skills):
                    cols[i % 3].error(skill)
            else:
                st.success("No major skill gaps.")

        with tab3:
            st.write(f"**Email:** {contact['email']}")
            st.write(f"**Phone:** {contact['phone']}")

        with tab4:
            for item in feedback:
                st.write(item)

        st.markdown("---")

        st.download_button(
            "Download Analysis Report",
            report_df.to_csv(index=False),
            file_name="resume_analysis.csv",
            mime="text/csv"
        )

        st.dataframe(report_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.caption("Built with ❤️ by Shivam Upadhyay")

    else:
        st.warning("Please upload a resume first.")
