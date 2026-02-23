def calculate_final_score(skill_score, experience_years):
    # Tiered Classification logic
    if experience_years == 0:
        candidate_type = "Fresher"
        final_score = skill_score * 0.8  # Skills matter most for freshers
    elif 0 < experience_years <= 2:
        candidate_type = "Junior / Entry Level"
        final_score = (skill_score * 0.7) + (experience_years * 5)
    elif 2 < experience_years <= 5:
        candidate_type = "Mid-Level Professional"
        final_score = (skill_score * 0.6) + (experience_years * 6)
    else:
        candidate_type = "Senior Professional"
        final_score = (skill_score * 0.5) + (experience_years * 7)

    # Score should not exceed 100
    return min(round(final_score, 2), 100), candidate_type, candidate_type
