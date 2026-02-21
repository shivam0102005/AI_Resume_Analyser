import pandas as pd

def generate_report(score, resume_skills, missing_skills):
    report = {
        "Match Score (%)": score,
        "Skills Found": ", ".join(resume_skills),
        "Missing Skills": ", ".join(missing_skills)
    }
    return pd.DataFrame([report])