import math
import re

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def calculate_match(resume, jd):
    res_tokens = tokenize(resume)
    jd_tokens = tokenize(jd)
    
    # Create frequency map of all unique words
    all_words = set(res_tokens).union(set(jd_tokens))
    res_vec = {word: res_tokens.count(word) for word in all_words}
    jd_vec = {word: jd_tokens.count(word) for word in all_words}
    
    # Cosine Similarity Math: (A.B) / (|A|*|B|)
    dot_product = sum(res_vec[word] * jd_vec[word] for word in all_words)
    res_mag = math.sqrt(sum(val**2 for val in res_vec.values()))
    jd_mag = math.sqrt(sum(val**2 for val in jd_vec.values()))
    
    if not res_mag or not jd_mag:
        return 0.0
        
    return round((dot_product / (res_mag * jd_mag)) * 100, 2)2)
