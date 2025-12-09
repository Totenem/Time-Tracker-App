import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database by running init.sql if tables don't exist"""
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        users_table_exists = cursor.fetchone()[0]
        
        if users_table_exists:
            print("Database tables already exist. Skipping initialization.")
            cursor.close()
            conn.close()
            return
        
        print("Database tables not found. Initializing database...")
        
        # Try to read init.sql first, fallback to seed.sql
        init_file_path = os.path.join(os.path.dirname(__file__), 'init.sql')
        if not os.path.exists(init_file_path):
            init_file_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
            if not os.path.exists(init_file_path):
                raise FileNotFoundError(f"Neither init.sql nor seed.sql found in {os.path.dirname(__file__)}")
        
        with open(init_file_path, 'r') as f:
            init_sql = f.read()
        
        # Execute the init SQL
        cursor.execute(init_sql)
        conn.commit()
        
        print("Database initialized successfully!")
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Database error during initialization: {e}")
        if conn:
            conn.rollback()
        raise
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
