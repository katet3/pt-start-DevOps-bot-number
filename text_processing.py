import re

def find_email(text):
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

def find_phone_number(text):
    pattern = r'(\+7|8)(\s*|-|\()?(\d{3})(\s*|-|\))?(\s*|-)?(\d{3})(\s*|-)?(\d{2})(\s*|-)?(\d{2})'
    results = re.findall(pattern, text)
    return [''.join(result) for result in results]
