from db.server import connect_to_db

def store_user(user: dict) -> bool:
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, username, email, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", (user["user_id"], user["username"], user["email"], user["password"], user["created_at"], user["updated_at"]))
        conn.commit()
        return True
    else:
        return False