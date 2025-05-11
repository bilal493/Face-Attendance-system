from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Backend.Database.db_connection import get_database_connection
from Student.add_student import Add_Student
from Backend.Email.send_email import send_email_notification  # ✅ Import email sender
import os
import numpy as np
import mysql.connector
import cv2
from time import strftime
from datetime import datetime


class Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x890+0+0")
        self.root.title("Face Attendance System")

        # title
        title = Label(self.root, text="Face Detector", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)

        b1 = Button(text="Detect", command=self.Detection, font=("", 15, "bold"), bg="lightgoldenrod3", cursor="hand2",
                    relief="groove")
        b1.place(x=1000, y=400, width=250, height=60)

    def mark_attendance(self, student_id, roll_no, name, department):
        try:
            connection = get_database_connection()
            my_cursor = connection.cursor()
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            my_cursor.execute("SELECT * FROM attendance WHERE student_id = %s AND date = %s", (student_id, date))
            existing_record = my_cursor.fetchone()

            if not existing_record:
                sql = "INSERT INTO attendance (student_id, time, date, status) VALUES (%s, %s, %s, %s)"
                values = (student_id, time, date, "Present")
                my_cursor.execute(sql, values)
                connection.commit()

                # Save recognized student ID to a file
                with open("recognized_student.txt", "w") as file:
                    file.write(student_id)

                # ✅ Send email to parent
                send_email_notification()

                messagebox.showinfo("Success", f"Attendance marked successfully for {name}.", parent=self.root)

            connection.close()

        except mysql.connector.Error as db_error:
            messagebox.showerror("Database Error", f"Error: {db_error}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected Error: {e}", parent=self.root)

    def Detection(self):
        def draw_boundary(img, classifier, scale, min_neighbour, color, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scale, min_neighbour)
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                connection = get_database_connection()
                my_cursor = connection.cursor()

                my_cursor.execute("SELECT student_id, name, student_rollno, dep FROM student WHERE student_id = %s",
                                  (id,))
                student_data = my_cursor.fetchone()

                if student_data and confidence > 77:
                    student_id, name, roll_no, department = student_data
                    cv2.putText(img, f"ID: {student_id}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255),
                                3)
                    cv2.putText(img, f"Roll no: {roll_no}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255),
                                3)
                    cv2.putText(img, f"Name: {name}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {department}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                                (255, 255, 255), 3)

                    self.mark_attendance(str(student_id), roll_no, name, department)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

        def recognize(img, clf, cascade):
            draw_boundary(img, cascade, 1.1, 10, (255, 255, 255), clf)
            return img

        faceCascade = cv2.CascadeClassifier(
            r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\Backend\Generate_Data\classifier.xml")
        video = cv2.VideoCapture(0)

        while True:
            ret, img = video.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Recognition(root)
    root.mainloop()
