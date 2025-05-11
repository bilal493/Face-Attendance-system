import csv
from Backend.Database.db_connection import get_database_connection

def export_attendance(student_id):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        # Fetch student details
        cursor.execute("SELECT name FROM student WHERE student_id = %s", (student_id,))
        student_name = cursor.fetchone()
        student_name = student_name[0] if student_name else "Unknown"

        # Write to CSV file (real-time export)
        with open("real_time_attendance.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([student_id, student_name])

        print(f"Exported: {student_id} - {student_name}")

        connection.close()

    except Exception as e:
        print(f"Error exporting attendance: {e}")
