from db.server import connect_to_db
from fastapi.responses import JSONResponse

def check_if_username_exists(username: str) -> bool:
    # check if the username is already taken
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    else:
        return JSONResponse(status_code=500, content={"message": "Database connection failed"})

def check_if_email_exists(email: str) -> bool:
    # check if the email is already taken
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    else:
        return JSONResponse(status_code=500, content={"message": "Database connection failed"})