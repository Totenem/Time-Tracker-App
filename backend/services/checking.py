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

def get_user(username: str) -> dict:
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            # Get column names from cursor description
            column_names = [desc[0] for desc in cursor.description]
            # Convert tuple to dictionary
            user_dict = dict(zip(column_names, result))
            return user_dict
        else:
            raise ValueError("User not found")
    else:
        raise ValueError("Database connection failed")

def get_project_id(project_name: str) -> int:
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM projects WHERE name = %s", (project_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    else:
        raise ValueError("Database connection failed")

def get_time_entries(user_id: str, start_date: str, end_date: str) -> list:
    from decimal import Decimal
    from datetime import datetime, date
    
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Join with projects table to get project name
        cursor.execute("""
            SELECT te.*, p.name as project_name 
            FROM time_entries te 
            JOIN projects p ON te.project_id = p.id 
            WHERE te.user_id = %s AND te.entry_date BETWEEN %s AND %s
            ORDER BY te.entry_date DESC
        """, (user_id, start_date, end_date))
        result = cursor.fetchall()
        if result:
            # Get column names from cursor description
            column_names = [desc[0] for desc in cursor.description]
            # Convert each row to dictionary and handle Decimal/datetime serialization
            time_entries_list = []
            for row in result:
                entry_dict = dict(zip(column_names, row))
                # Convert non-JSON-serializable types for JSON serialization
                for key, value in entry_dict.items():
                    if isinstance(value, Decimal):
                        entry_dict[key] = float(value)
                    elif isinstance(value, (datetime, date)):
                        entry_dict[key] = value.isoformat()
                time_entries_list.append(entry_dict)
            return time_entries_list
        else:
            return []
    else:
        raise ValueError("Database connection failed")

def get_time_entries_by_project(user_id: str, start_date: str, end_date: str, project_id: int) -> list:
    from decimal import Decimal
    from datetime import datetime, date
    
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        # Join with projects table to get project name
        cursor.execute("""
            SELECT te.*, p.name as project_name 
            FROM time_entries te 
            JOIN projects p ON te.project_id = p.id 
            WHERE te.user_id = %s AND te.entry_date BETWEEN %s AND %s AND te.project_id = %s
            ORDER BY te.entry_date DESC
        """, (user_id, start_date, end_date, project_id))
        result = cursor.fetchall()
        if result:
            # Get column names from cursor description
            column_names = [desc[0] for desc in cursor.description]
            # Convert each row to dictionary and handle Decimal/datetime serialization
            time_entries_list = []
            for row in result:
                entry_dict = dict(zip(column_names, row))
                # Convert non-JSON-serializable types for JSON serialization
                for key, value in entry_dict.items():
                    if isinstance(value, Decimal):
                        entry_dict[key] = float(value)
                    elif isinstance(value, (datetime, date)):
                        entry_dict[key] = value.isoformat()
                time_entries_list.append(entry_dict)
            return time_entries_list
        else:
            return []
    else:
        raise ValueError("Database connection failed")

def get_project_totals(user_id: str, start_date: str, end_date: str) -> dict:
    from decimal import Decimal
    
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name as project_name, SUM(te.hours) as total_hours
            FROM time_entries te
            JOIN projects p ON te.project_id = p.id
            WHERE te.user_id = %s AND te.entry_date BETWEEN %s AND %s
            GROUP BY p.name
            ORDER BY total_hours DESC
        """, (user_id, start_date, end_date))
        result = cursor.fetchall()
        if result:
            project_totals = {}
            for row in result:
                project_name = row[0]
                total_hours = row[1]
                # Convert Decimal to float
                if isinstance(total_hours, Decimal):
                    total_hours = float(total_hours)
                project_totals[project_name] = total_hours
            return project_totals
        else:
            return {}
    else:
        raise ValueError("Database connection failed")