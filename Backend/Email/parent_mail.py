from Backend.Database.db_connection import get_database_connection

def fetch_parent_email():
    try:
        with open(r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\Frontend\recognized_student.txt", "r") as file:
            student_id = file.read().strip()

        if not student_id:
            print("No student recognized.")
            return None

        connection = get_database_connection()
        my_cursor = connection.cursor()
        my_cursor.execute("SELECT parent_email FROM student WHERE student_id = %s", (student_id,))
        parent_email = my_cursor.fetchone()

        connection.close()

        if parent_email:
            print(f"✅ Parent email fetched for student_id {student_id}: {parent_email[0]}")
            return parent_email[0]
        else:
            print(f"❌ No parent email found for student_id {student_id}")
            return None

    except FileNotFoundError:
        print("recognized_student.txt not found. Run recognition.py first.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
