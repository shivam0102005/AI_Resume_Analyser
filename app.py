import streamlit as st
import pandas as pd
from utils.extractor import extract_text
from utils.preprocessing import clean_text, lemmatize, extract_experience

from utils.intelligence import auto_detect_industry, extract_contact_info, get_skills_by_industry, analyze_skill_gap
from utils.scorer import calculate_final_score
from utils.report_generator import generate_report

# 1. Page Config & Hide Deploy/Menu
st.set_page_config(page_title="AI Resume Intelligence", page_icon="🎯", layout="wide")

# CSS to hide "Deploy" button and "Streamlit Menu"
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F8FAFC; }
    .main-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .main-title {
        color: #1E293B;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Header
st.markdown('<h1 class="main-title">AI Resume Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#64748B;">Autonomous Applicant Screening System</p>', unsafe_allow_html=True)

# 3. Input Section
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### 📄 Resume Upload")
    # key="unique_resume_uploader" ensures no duplicate ID error
    resume_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"], label_visibility="collapsed", key="unique_resume_uploader")
    st.markdown('</div>', unsafe_allow_html=True)

analyze_btn = st.button("Generate Match Intelligence", use_container_width=True, type="primary")

# 4. Logic Execution
if analyze_btn:
    if resume_file:
        with st.spinner("AI is analyzing the resume..."):
            resume_raw = extract_text(resume_file)
            industry = auto_detect_industry(resume_raw)
            contact = extract_contact_info(resume_raw)
            experience_years = extract_experience(resume_raw)
            resume_skills = get_skills_by_industry(resume_raw, industry)
            missing_skills = analyze_skill_gap(resume_skills, industry)
            
            skill_base_score = min(len(resume_skills) * 8, 100)
            final_score, candidate_type = calculate_final_score(skill_base_score, experience_years)
            report_df = generate_report(final_score, resume_skills, missing_skills)

        # 5. Results Dashboard
        st.markdown("---")
        st.subheader(f"📊 Analysis Results: {industry}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MATCH SCORE", f"{final_score}%")
        with col2:
            st.metric("CANDIDATE TYPE", candidate_type)
        with col3:
            st.metric("WORK EXPERIENCE", f"{experience_years} Years")

        tab1, tab2, tab3 = st.tabs(["🎯 Identified Skills", "❌ Missing Keywords", "📞 Contact Details"])
        
        with tab1:
            if resume_skills:
                cols = st.columns(3)
                for i, skill in enumerate(resume_skills):
                    cols[i % 3].markdown(f"✅ **{skill}**")
            else:
                st.info("No industry-specific skills detected.")

        with tab2:
            if missing_skills:
                for s in missing_skills:
                    st.markdown(f"- <span style='color:#DC2626'>{s}</span>", unsafe_allow_html=True)
            else:
                st.success("Perfect Match! All key industry skills found.")

        with tab3:
            st.write(f"**Email:** {contact['email']}")
            st.write(f"**Phone:** {contact['phone']}")
            
        st.dataframe(report_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Please upload a resume first.")

