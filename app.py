import streamlit as st
from utils.extractor import extract_text
from utils.preprocessing import clean_text, lemmatize
from utils.matcher import calculate_match
from utils.skills import extract_skills, find_missing
from utils.report_generator import generate_report

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer")
st.write("Production Level Resume Screening System")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)")
jd_text = st.text_area("Paste Job Description Here")

if resume_file and jd_text:

    with st.spinner("Analyzing Resume..."):
        resume_text = extract_text(resume_file)
        resume_text = lemmatize(clean_text(resume_text))
        jd_text_clean = lemmatize(clean_text(jd_text))

        score = calculate_match(resume_text, jd_text_clean)

        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills(jd_text_clean)
        missing = find_missing(resume_skills, jd_skills)

        report_df = generate_report(score, resume_skills, missing)

    st.success("Analysis Complete ✅")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Match Score", f"{score}%")

    with col2:
        st.write("### Missing Skills")
        st.write(missing)

    st.write("### Full Report")
    st.dataframe(report_df)

    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Report",
        csv,
        "resume_analysis_report.csv",
        "text/csv"
    )