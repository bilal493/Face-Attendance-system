from Backend.Database.db_connection import get_database_connection


def fetch_attendance_data():
    try:
        connection = get_database_connection()
        my_cursor = connection.cursor()

        my_cursor.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")
        data = my_cursor.fetchall()

        connection.commit()
        connection.close()
        return data

    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        return []
