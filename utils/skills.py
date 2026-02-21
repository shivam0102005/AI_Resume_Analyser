
from config import SKILLS_DB

def extract_skills(text):
    found = []
    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)
    return list(set(found))

def find_missing(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))