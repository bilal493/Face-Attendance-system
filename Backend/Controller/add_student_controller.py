from tkinter import messagebox
import mysql.connector
from Backend.Database.db_connection import get_database_connection

def add_data_to_database(dep, shift, year, student_rollno, std_id, std_name, gender, std_email, phone, parent_email, address, photo_sample, parent_window):
    if dep == "Select Department" or std_id == "" or std_name == "":
        messagebox.showerror("Error", "All Fields are required", parent=parent_window)
    else:
        try:
            connection = get_database_connection()
            my_cursor = connection.cursor()

            # Execute the query
            my_cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                dep, shift, year, student_rollno, std_id, std_name, gender, std_email, phone, parent_email, address, photo_sample
            ))

            # Commit and close
            connection.commit()
            connection.close()

            # Success message
            messagebox.showinfo("Success", "Student Details have been added Successfully", parent=parent_window)
        except mysql.connector.Error as db_error:
            print(f"Database Error: {db_error}")
            messagebox.showerror("Database Error", f"Due to: {db_error}", parent=parent_window)
        except Exception as e:
            print(f"Unexpected Error: {e}")
            messagebox.showerror("Error", f"Unexpected Error: {e}", parent=parent_window)
