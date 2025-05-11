from Backend.Database.db_connection import get_database_connection

def fetch_student_data():

    try:
        connection = get_database_connection()  # Get the database connection
        my_cursor = connection.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()  # Fetch all student records
        connection.commit()
        connection.close()
        return data
    except Exception as e:
        print(f"Error fetching student data: {e}")
        raise
