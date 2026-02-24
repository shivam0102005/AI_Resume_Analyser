import re

from datetime import datetime


# 1. Clean Text Function (Jiske bina error aa raha hai)
def clean_text(text):
    # Manual cleaning using Regex: lowercase and remove special characters
    text = text.lower()

    # Special characters hatao par dash (-) rakho dates ke liye
    text = re.sub(r'[^a-z0-9\s.+#-]', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())

# 2. Lemmatize Function
def lemmatize(text):
    words = text.split()
    stemmed = []
    for word in words:
        if len(word) > 4:
            if word.endswith('ing'): word = word[:-3]
            elif word.endswith('ed'): word = word[:-2]
            elif word.endswith('es'): word = word[:-2]
            elif word.endswith('s'): word = word[:-1]
        stemmed.append(word)
    return " ".join(stemmed)



import re
from datetime import datetime

def extract_experience(text):
    """
    Hybrid Extractor:
    1. Pehle 'X+ years' jaise keywords dhoondta hai.
    2. Phir date ranges (2022-2024) calculate karta hai.
    3. Dono mein se jo zyada ho, wo return karta hai.
    """
    text_clean = text.replace('\n', ' ')
    
    # --- METHOD 1: Direct Keyword Matching (3+ years, 5 year exp) ---
    # Ye pattern '3+ years', '5 years', '4.5 year' sab pakad lega
    keyword_pattern = r'(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:year|yrs|years)\s*(?:of)?\s*(?:experience|exp)?'
    keyword_matches = re.findall(keyword_pattern, text_clean.lower())
    
    max_from_keywords = 0
    if keyword_matches:
        max_from_keywords = max([float(x) for x in keyword_matches])

    # --- METHOD 2: Date Range Calculation (2022-2024) ---
    total_months_from_dates = 0
    # Sirf Work Experience section ko target karo taaki Education dates na aayein
    sections = re.split(r'(?i)(?:WORK|EXPERIENCE|EMPLOYMENT|JOB|ROLES)', text)
    relevant_text = sections[1] if len(sections) > 1 else text
    relevant_text = re.split(r'(?i)(?:EDUCATION|PROJECTS|SKILLS|ACADEMIC)', relevant_text)[0]

    # Pattern for: 2022-2024, Jan 2020 - Present, 05/2019 to 08/2021
    date_pattern = r'([A-Za-z]{3,9}\s+\d{4}|\d{1,2}/\d{2,4}|\b\d{4}\b)\s*(?:-|to|–|till|present)\s*([A-Za-z]{3,9}\s+\d{4}|\d{1,2}/\d{2,4}|\b\d{4}\b|Present|Current|Now)'
    date_matches = re.findall(date_pattern, relevant_text, re.IGNORECASE)

    for start, end in date_matches:
        try:
            start_dt = parse_simple_date(start)
            if any(x in end.lower() for x in ['present', 'current', 'now', 'till']):
                end_dt = datetime.now()
            else:
                end_dt = parse_simple_date(end)
            
            if start_dt and end_dt and end_dt > start_dt:
                diff = (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month)
                total_months_from_dates += diff
        except:
            continue

    max_from_dates = round(total_months_from_dates / 12, 1)

    # --- FINAL DECISION ---
    # Agar resume mein likha hai "3+ years" par dates se 4 saal ban rahe hain, toh 4 dikhayega
    return max(max_from_keywords, max_from_dates)

def parse_simple_date(date_str):
    date_str = date_str.strip()
    # Sirf Year (2022) ko handling
    if len(date_str) == 4 and date_str.isdigit():
        return datetime(int(date_str), 1, 1)
        
    formats = ["%b %Y", "%B %Y", "%m/%Y", "%m/%y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            continue
    return None

import re
from datetime import datetime

def extract_experience(text):

    text_lower = text.lower()

    # Only consider experience-related sections
    if "work experience" not in text_lower and "experience" not in text_lower:
        return 0

    # Extract only part after "experience"
    split_text = re.split(r'work experience|experience', text_lower)
    if len(split_text) > 1:
        section = split_text[1]
    else:
        section = text_lower

    # Stop at education
    section = re.split(r'education|skills|projects', section)[0]

    # Detect year ranges
    range_pattern = r'(20\d{2})\s*(?:-|to|–)\s*(20\d{2}|present|current|now)'
    matches = re.findall(range_pattern, section)

    total_years = 0

    for start, end in matches:
        start = int(start)

        if end in ["present", "current", "now"]:
            end = datetime.now().year
        else:
            end = int(end)

        if end > start:
            total_years += (end - start)

    return total_years
