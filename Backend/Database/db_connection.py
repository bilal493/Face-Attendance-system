# db_connection.py
import mysql.connector
from mysql.connector import Error

def get_database_connection():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pa$$WORD",
            database="face-attendance",
            port="3306",
            auth_plugin="mysql_native_password"
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        raise
