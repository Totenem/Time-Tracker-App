import re

def validate_password(password: str) -> str:
    # check if the password is at least 8 characters long
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    # check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter")
    # check if the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lowercase letter")
    # check if the password contains at least one number
    if not re.search(r'[0-9]', password):
        raise ValueError("Password must contain at least one number")
    return password