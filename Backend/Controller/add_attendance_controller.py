import mysql.connector
from Backend.Database.db_connection import get_database_connection
from tkinter import messagebox


def add_attendance_to_database(student_id, time, date, status, parent_window):
    if not student_id or not time or not date or not status:
        messagebox.showerror("Error", "All Fields are required", parent=parent_window)
        return

    try:
        connection = get_database_connection()
        my_cursor = connection.cursor()

        sql = "INSERT INTO attendance (student_id, time, date, status) VALUES (%s, %s, %s, %s)"
        values = (student_id, time, date, status)

        my_cursor.execute(sql, values)
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Attendance recorded successfully!", parent=parent_window)

    except mysql.connector.Error as db_error:
        messagebox.showerror("Database Error", f"Error: {db_error}", parent=parent_window)

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected Error: {e}", parent=parent_window)
