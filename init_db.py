import mysql.connector
from config import Config
import os

def init_db():
    # Connect to MySQL Server (no DB selected yet)
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        print(f"Database '{Config.MYSQL_DB}' created or already exists.")
        
        # Connect to the specific database
        conn.database = Config.MYSQL_DB
        
        # Helper to execute file
        def execute_sql_file(filename):
            print(f"Executing {filename}...")
            with open(filename, 'r') as f:
                # Split by semicolon for basic parsing (simple approach)
                # Note: This is a simple splitter, might break on complex stored procs but fine for simple schema
                sql_file = f.read()
                commands = sql_file.split(';')
                for command in commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                        except mysql.connector.Error as err:
                            print(f"Skipping command due to error: {err}")
            
        execute_sql_file('schema.sql')
        execute_sql_file('dummy_data.sql')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialization complete.")
        
    except mysql.connector.Error as err:
        print(f"Error initializing database: {err}")

if __name__ == '__main__':
    init_db()
