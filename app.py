import streamlit as st
import pandas as pd
from utils.extractor import extract_text
from utils.preprocessing import clean_text, lemmatize, extract_experience
from utils.matcher import calculate_match
from utils.skills import extract_skills, find_missing
from utils.scorer import calculate_final_score
from utils.report_generator import generate_report

# 1. Page Config
st.set_page_config(page_title="AI Resume Intelligence", page_icon="🎯", layout="wide")

# 2. Professional CSS Styling
st.markdown("""
    <style>
    /* Hide Streamlit elements */
    .stAppDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    footer { visibility: hidden; }
    
    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Professional Card Styling */
    .main-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Custom Title */
    .main-title {
        color: #1E293B;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.markdown('<h1 class="main-title">AI Resume Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enterprise-grade applicant screening & matching system</p>', unsafe_allow_html=True)

# 4. Input Section in a professional layout
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📄 Resume Upload")
        resume_file = st.file_uploader("Drop your PDF or DOCX here", type=["pdf", "docx"], label_visibility="collapsed")
        st.caption("Supported formats: PDF, DOCX (Max 200MB)")

    with col2:
        st.markdown("### 📝 Job Description")
        jd_text = st.text_area("Enter the requirements to match against", height=150, placeholder="Paste JD here...", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 5. Action Button
st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("Generate Match Intelligence", use_container_width=True, type="primary")

# 6. Logic Execution
if analyze_btn:
    if resume_file and jd_text:
        with st.spinner("Processing NLP Models..."):
            # Extraction & Manual NLP Logic (No external libraries)
            resume_raw = extract_text(resume_file)
            resume_clean = lemmatize(clean_text(resume_raw))
            jd_clean = lemmatize(clean_text(jd_text))

            score = calculate_match(resume_clean, jd_clean)
            resume_skills = extract_skills(resume_clean)
            jd_skills = extract_skills(jd_clean)
            missing = find_missing(resume_skills, jd_skills)
            
            experience_years = extract_experience(resume_raw)
            final_score, candidate_type = calculate_final_score(score, experience_years)
            
            report_df = generate_report(final_score, resume_skills, missing)

        # 7. Results Dashboard
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            st.markdown(f'<div style="text-align:center; padding:20px; border-radius:10px; border: 1px solid #E2E8F0;">'
                        f'<p style="color:#64748B; font-size:14px; margin:0;">MATCH SCORE</p>'
                        f'<h2 style="color:#2563EB; margin:0;">{final_score}%</h2>'
                        f'</div>', unsafe_allow_html=True)
        
        with m_col2:
            st.markdown(f'<div style="text-align:center; padding:20px; border-radius:10px; border: 1px solid #E2E8F0;">'
                        f'<p style="color:#64748B; font-size:14px; margin:0;">CANDIDATE TYPE</p>'
                        f'<h2 style="color:#1E293B; margin:0;">{candidate_type}</h2>'
                        f'</div>', unsafe_allow_html=True)
            
        with m_col3:
            st.markdown(f'<div style="text-align:center; padding:20px; border-radius:10px; border: 1px solid #E2E8F0;">'
                        f'<p style="color:#64748B; font-size:14px; margin:0;">WORK EXPERIENCE</p>'
                        f'<h2 style="color:#059669; margin:0;">{experience_years} Years</h2>'
                        f'</div>', unsafe_allow_html=True)

        # Detailed Breakdowns
        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🎯 Skill Gap Analysis", "📄 Comprehensive Data"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.write("### ✅ Identified Skills")
                if resume_skills:
                    for s in resume_skills:
                        st.markdown(f"- **{s.title()}**")
                else:
                    st.info("No common skills detected.")
            
            with c2:
                st.write("### ❌ Missing Skills")
                if missing:
                    for s in missing:
                        st.markdown(f"- <span style='color:#DC2626'>{s.title()}</span>", unsafe_allow_html=True)
                else:
                    st.success("Perfect Match! All JD skills found.")

        with tab2:
            st.dataframe(report_df, use_container_width=True, hide_index=True)

    else:
        st.warning("⚠️ Please provide both a Resume and a Job Description to begin.")
