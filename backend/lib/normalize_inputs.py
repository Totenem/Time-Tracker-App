import re

def normalize_username(username: str) -> str:
    # remove whitespace
    username = username.strip()
    if username == re.match(r'^[a-zA-Z0-9]+$', username):
        return username.lower()
    else:
        raise ValueError("Username must contain only letters and numbers")

def normalize_email(email: str) -> str:
    # remove whitespace
    email = email.strip()
    if email == re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return email.lower()
    else:
        raise ValueError("Email is not valid")