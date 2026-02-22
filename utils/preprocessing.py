import re

def clean_text(text):
    # Manual cleaning using Regex: lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return ' '.join(text.split())

def lemmatize(text):
    # Simple manual suffix stripping (Basic Stemming)
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

def extract_experience(text):
    text = text.lower()
    
    # 1. Check for Years (e.g., "2 years", "3 yrs")
    year_matches = re.findall(r'(\d+)\s*(?:year|yr)s?', text)
    
    # 2. Check for Months (e.g., "6 months", "1 month")
    month_matches = re.findall(r'(\d+)\s*month', text)
    
    total_years = 0
    
    if year_matches:
        # Take the highest year mentioned
        total_years = max([int(y) for y in year_matches])
        
    if month_matches:
        # Convert months to years (e.g., 1 month = 0.08 years)
        max_months = max([int(m) for m in month_matches])
        month_contribution = max_months / 12
        
        # If no years were found, just use the month fraction
        if total_years == 0:
            total_years = month_contribution
            
    return round(total_years, 2)
