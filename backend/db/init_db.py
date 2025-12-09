import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database by running seed.sql if tables don't exist"""
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
        
        # Read and execute seed.sql
        seed_file_path = os.path.join(os.path.dirname(__file__), 'seed.sql')
        with open(seed_file_path, 'r') as f:
            seed_sql = f.read()
        
        # Execute the seed SQL
        cursor.execute(seed_sql)
        conn.commit()
        
        print("Database initialized successfully!")
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
            conn.close()
        raise
    except Exception as e:
        print(f"Unexpected error during database initialization: {e}")
        raise
