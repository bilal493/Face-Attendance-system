from tkinter import messagebox

import cv2

from Backend.Controller.fetch_data_controller import fetch_student_data
from Backend.Database.db_connection import get_database_connection


def fetch_data(self):
    try:
        # Get student data from the separated logic
        data = fetch_student_data()

        # Populate the table if data is not empty
        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())  # Clear existing data
            for record in data:
                self.student_table.insert("", "end", values=record)  # Insert new data
    except Exception as e:
        print(f"Error in fetch_data method: {e}")

def reset_data(self):
    self.var_dep.set("Select Department")
    self.var_shift.set("Select Shift")
    self.var_year.set("Select year"),
    self.var_std_id.set(""),
    self.var_std_name.set(""),
    self.var_gender.set("Select"),
    self.var_std_email.set(""),
    self.var_phone.set(""),
    self.var_parent_email.set(""),
    self.var_address.set(""),

def generate_dataset(self):
    if self.var_dep.get() == "Select Department" or self.var_std_id.get() == "" or self.var_std_name.get() == "":
        messagebox.showerror("Error", "All Fields are required", parent=self.root)
    else:
        try:
            connection = get_database_connection()
            my_cursor = connection.cursor()

            # Update student details in the database
            sql_query = """
                UPDATE student 
                SET dep=%s, shift=%s, year=%s, name=%s, gender=%s, student_email=%s, phone=%s, parent_email=%s, address=%s 
                WHERE student_id=%s
            """
            data = (
                self.var_dep.get(),
                self.var_shift.get(),
                self.var_year.get(),
                self.var_std_name.get(),
                self.var_gender.get(),
                self.var_std_email.get(),
                self.var_phone.get(),
                self.var_parent_email.get(),
                self.var_address.get(),
                self.var_std_id.get()
            )
            my_cursor.execute(sql_query, data)
            connection.commit()
            self.fetch_data()
            # self.reset_data()
            connection.close()

            # Load haarcascade file
            face_classifier = cv2.CascadeClassifier(r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\haarcascade_frontalface_default.xml")

            # Pre-processing
            def face_crop(img):
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray_img, 1.3, 5)
                for (x, y, w, h) in faces:
                    crop_image = img[y:y+h, x:x+w]
                    return crop_image

            capture_video = cv2.VideoCapture(0)
            img_id = 0
            student_id = self.var_std_id.get()  # Use student ID for unique filenames
            while True:
                ret, my_frame = capture_video.read()
                if face_crop(my_frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_crop(my_frame), (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGRA2BGR)
                    # Save the image using student ID
                    file_path = rf"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\Backend\Generate_Data\data\user.{student_id}.{img_id}.jpg"
                    cv2.imwrite(file_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Crop Image", face)

                if cv2.waitKey(1) == 13 or int(img_id) == 100:
                    break

            capture_video.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Data Generation Completed")

        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


