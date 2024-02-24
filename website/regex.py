import re

# Define Regex patterns
email_pattern = re.compile(r"[A-Za-z0-9]+@[A-Za-z]+\.[A-Za-z]+", re.IGNORECASE)
services_pattern = re.compile(r"t[0-9]+@services\.idf", re.IGNORECASE)

# Check match
def check_regex(input):
    if re.fullmatch(email_pattern, input):
        return True
    
    else:
        return False