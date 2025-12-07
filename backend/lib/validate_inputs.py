import re
from fastapi.responses import JSONResponse

def validate_password(password: str) -> JSONResponse:
    # check if the password is at least 8 characters long
    if len(password) < 8:
        return JSONResponse(status_code=400, content={"message": "Password must be at least 8 characters long"})
    # check if the password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return JSONResponse(status_code=400, content={"message": "Password must contain at least one uppercase letter"})
    # check if the password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return JSONResponse(status_code=400, content={"message": "Password must contain at least one lowercase letter"})
    # check if the password contains at least one number
    if not re.search(r'[0-9]', password):
        return JSONResponse(status_code=400, content={"message": "Password must contain at least one number"})
    return JSONResponse(status_code=200, content={"message": "Password is valid"})