import re
from utils.big_data import TRAINING_KNOWLEDGE

def auto_detect_industry(text):
    text_lower = text.lower()
    scores = {dept: 0 for dept in TRAINING_KNOWLEDGE.keys()}
    for dept, skills in TRAINING_KNOWLEDGE.items():
        for skill in skills:
            if re.search(rf'\b{re.escape(skill.lower())}\b', text_lower):
                scores[dept] += 1
    return max(scores, key=scores.get) if any(scores.values()) else "Data Science & Analytics"

def extract_contact_info(text):
    """
    Ekdam simple aur robust logic: 
    Pehle saare numbers dhoondo, phir Aadhaar ko manual check se hatao.
    """
    # 1. Email Extraction
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    
    # 2. Phone Extraction
    # Ye pattern sirf digits, plus, dashes aur slashes dhoondega (length 10 se 15)
    # Isse +91-9161265404/9703916126 poora segment mil jayega
    raw_pattern = r'[\+\d][\d\s\-\/\(\)]{9,25}'
    all_matches = re.findall(raw_pattern, text)
    
    final_phones = []
    for match in all_matches:
        # Segment ko split karo agar slash (/) hai
        parts = re.split(r'[/|,]', match)
        for p in parts:
            p_clean = p.strip()
            # Sirf digits nikalo counting ke liye
            digits = re.sub(r'\D', '', p_clean)
            
            # Agar 10 se 13 digits hain, toh ye Mobile Number hai
            if 10 <= len(digits) <= 13:
                # Aadhaar Filter: Agar text mein us number ke aas-paas 'Aadhaar' hai toh skip
                start_idx = text.find(p_clean)
                context = text[max(0, start_idx-30) : start_idx].lower()
                
                if "aadhaar" not in context and "aadhar" not in context:
                    if p_clean not in final_phones:
                        final_phones.append(p_clean)

    return {
        "email": emails[0] if emails else "Not Found",
        "phone": " / ".join(final_phones) if final_phones else "Not Found"
    }

def get_skills_by_industry(text, industry):
    """Industry specific skills extraction logic"""
    text_norm = f" {text.lower()} ".replace('-', ' ')
    found = []
    # TRAINING_KNOWLEDGE se skills load karo
    search_list = TRAINING_KNOWLEDGE.get(industry, [])
    if not search_list:
        search_list = [s for sk in TRAINING_KNOWLEDGE.values() for s in sk]
        
    for skill in search_list:
        skill_clean = skill.lower().replace('-', ' ')
        pattern = rf'(?<![\w]){re.escape(skill_clean)}(?![\w])'
        if re.search(pattern, text_norm):
            found.append(skill.title())
    return list(set(found))

def analyze_skill_gap(found_skills, industry):
    """Missing skills identifying logic"""
    if industry in TRAINING_KNOWLEDGE:
        all_skills = [s.title() for s in TRAINING_KNOWLEDGE[industry]]
        missing = [s for s in all_skills if s.lower() not in [fs.lower() for fs in found_skills]]
        return missing[:5]
    return []
