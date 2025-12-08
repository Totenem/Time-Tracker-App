from db.server import connect_to_db

def store_user(user: dict) -> bool:
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, username, email, password_hash, created_at) VALUES (%s, %s, %s, %s, %s)", (user["user_id"], user["username"], user["email"], user["password"], user["created_at"]))
        conn.commit()
        return True
    else:
        return False