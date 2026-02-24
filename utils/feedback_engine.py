def generate_feedback(skill_score, experience_years, missing_skills, keyword_density):

    feedback = []

    # Skill based feedback
    if skill_score < 50:
        feedback.append("⚠ Add more relevant technical skills.")
    else:
        feedback.append("✅ Strong technical skill foundation detected.")

    # Experience feedback
    if experience_years == 0:
        feedback.append("⚠ No professional experience detected. Add internships or projects.")
    elif experience_years < 2:
        feedback.append("⚠ Entry-level experience detected. Add measurable achievements.")
    else:
        feedback.append("✅ Solid professional experience.")

    # Missing skills
    if missing_skills:
        feedback.append(f"⚠ Consider adding: {', '.join(missing_skills[:3])}")

    # Keyword density
    if keyword_density < 20:
        feedback.append("⚠ Resume lacks keyword optimization for ATS systems.")
    else:
        feedback.append("✅ Good keyword optimization.")

    return feedback
