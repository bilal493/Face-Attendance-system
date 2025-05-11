from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from Frontend.Student.student_details import Student_Details
from tkinter import messagebox
from Backend.Controller.add_student_controller import add_data_to_database
import mysql.connector
from Backend.Database.db_connection import get_database_connection
from Backend.Controller.fetch_data_controller import fetch_student_data
from Backend.Generate_Data.generate_data import generate_dataset



class Update_Student:
    def __init__(self, root, student_data=None):
        self.root = root
        self.root.geometry("1530x890+0+0")
        self.root.title("Face Attendance System")

        # -----------variables---------
        self.var_dep = StringVar()
        self.var_shift = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_std_id = StringVar()
        self.var_std_rno = StringVar()
        self.var_std_name = StringVar()
        self.var_gender = StringVar()
        self.var_std_email = StringVar()
        self.var_phone = StringVar()
        self.var_parent_email = StringVar()
        self.var_address = StringVar()

        if student_data:
            self.var_dep.set(student_data[0])
            self.var_shift.set(student_data[1])
            self.var_year.set(student_data[2])
            self.var_std_rno.set(student_data[3])
            self.var_std_id.set(student_data[4])
            self.var_std_name.set(student_data[5])
            self.var_gender.set(student_data[6])
            self.var_std_email.set(student_data[7])
            self.var_phone.set(student_data[8])
            self.var_parent_email.set(student_data[9])
            self.var_address.set(student_data[10])

        # background
        bg = Label(self.root, bg="floralwhite")
        bg.place(x=0, y=0, width=1530, height=890)

        # title
        title = Label(self.root, text="Student Management", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)


        #frame
        main_frame = Frame(bg, bd=5, bg="")
        main_frame.place(x=10, y=200, width=1500, height=600)

        title = Label(main_frame, text="Update Student", font=("", 15, "bold"), fg="white", bg="lightgoldenrod4")
        title.place(x=380, y=10, width=780, height=30)

        # course frame
        course_frame = LabelFrame(main_frame, bd=1, bg="white", relief=RIDGE, text="Course Details", font=("", 10))
        course_frame.place(x=380, y=55, width=780, height=160)

        # Department
        dep_label = Label(course_frame, text="Department:", font=("", 12, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, pady=25)

        dep_combo = ttk.Combobox(course_frame, textvariable=self.var_dep, font=("", 11), state="readonly")
        dep_combo["values"] = ("Select Department", "IT", "Law", "BBA", "English", "Commerce")
        dep_combo.grid(row=0, column=1, padx=2, pady=10)

        # shift
        shift_label = Label(course_frame, text="Shift:", font=("", 12, "bold"), bg="white")
        shift_label.grid(row=0, column=2, padx=30)

        shift_combo = ttk.Combobox(course_frame, textvariable=self.var_shift, font=("", 11), state="readonly")
        shift_combo["values"] = ("Select Shift", "Morning", "Afternoon")
        shift_combo.grid(row=0, column=3, padx=0, pady=10)

        # Year
        year_label = Label(course_frame, text="Year:", font=("", 12, "bold"), bg="white")
        year_label.grid(row=2, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(course_frame, textvariable=self.var_year, font=("", 11), state="readonly")
        year_combo["values"] = ("Select year", "2021-25", "2022-26", "2023-27", "2024-28", "2025-29", "2026-30")
        year_combo.grid(row=2, column=1, padx=2, pady=0)

        # Student class frame
        class_frame = LabelFrame(main_frame, bd=1, bg="white", relief=RIDGE, text="Student Class Details",
                                 font=("", 10))
        class_frame.place(x=380, y=220, width=780, height=360)

        # Student ID
        studentId_label = Label(class_frame, text="Student Id:", font=("", 12, "bold"), bg="white")
        studentId_label.grid(row=0, column=2, padx=5, pady=25, sticky=W)

        studentId_entry = ttk.Entry(class_frame, textvariable=self.var_std_id, width=30, font=("", 11))
        studentId_entry.grid(row=0, column=3, padx=10, sticky=W)

        # Student Roll #
        studentRno_label = Label(class_frame, text="Student Roll #", font=("", 12, "bold"), bg="white")
        studentRno_label.grid(row=0, column=0, padx=5, pady=25, sticky=W)

        studentRno_entry = ttk.Entry(class_frame, textvariable=self.var_std_rno, width=30, font=("", 11))
        studentRno_entry.grid(row=0, column=1, padx=10, sticky=W)

        # Student Name
        studentName_label = Label(class_frame, text="Student Name:", font=("", 12, "bold"), bg="white")
        studentName_label.grid(row=1, column=0, pady=5, sticky=W)

        studentName_entry = ttk.Entry(class_frame, textvariable=self.var_std_name, width=30, font=("", 11))
        studentName_entry.grid(row=1, column=1, padx=10, sticky=W)

        # Gender
        Gender_label = Label(class_frame, text="Gender:", font=("", 12, "bold"), bg="white")
        Gender_label.grid(row=1, column=2, padx=5, sticky=W)

        Gender_combo = ttk.Combobox(class_frame, textvariable=self.var_gender, width=28, font=("", 11),
                                    state="readonly")
        Gender_combo["values"] = ("Select", "Male", "Female")
        Gender_combo.current(0)
        Gender_combo.grid(row=1, column=3, padx=10, sticky=W)

        # Student Email
        Student_email_label = Label(class_frame, text="Student Email:", font=("", 12, "bold"), bg="white")
        Student_email_label.grid(row=2, column=0, pady=5, sticky=W)

        Student_email_entry = ttk.Entry(class_frame, textvariable=self.var_std_email, width=30, font=("", 11))
        Student_email_entry.grid(row=2, column=1, padx=10, sticky=W)

        # Phone number
        phone_label = Label(class_frame, text="Phone #:", font=("", 12, "bold"), bg="white")
        phone_label.grid(row=2, column=2, padx=5, pady=25, sticky=W)

        phone_entry = ttk.Entry(class_frame, textvariable=self.var_phone, width=30, font=("", 11))
        phone_entry.grid(row=2, column=3, padx=10, sticky=W)

        # Parent Email
        parent_email_label = Label(class_frame, text="Parent Email:", font=("", 12, "bold"), bg="white")
        parent_email_label.grid(row=3, column=2, pady=5, sticky=W)

        parent_email_entry = ttk.Entry(class_frame, textvariable=self.var_parent_email, width=30, font=("", 11))
        parent_email_entry.grid(row=3, column=3, padx=10, sticky=W)

        # Address
        address_label = Label(class_frame, text="Address:", font=("", 12, "bold"), bg="white")
        address_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        address_entry = ttk.Entry(class_frame, textvariable=self.var_address, width=30, font=("", 11))
        address_entry.grid(row=3, column=1, padx=10, sticky=W)

        #radio frame
        radio_frame = Frame(class_frame, bd=0, relief=RIDGE, bg="white")
        radio_frame.place(x=0, y=230, width=778, height=30)

        # radio_title = Label(radio_frame, text="Select:", font=("", 11, "bold"), fg="black", bg="white")
        # radio_title.grid(row=0, column=0, padx=5, sticky=W)
        #
        # # radio button
        # self.var_radio1 = StringVar()
        # radio_btn1 = ttk.Radiobutton(radio_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        # radio_btn1.grid(row=0, column=1)
        #
        # radio_btn2 = ttk.Radiobutton(radio_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        # radio_btn2.grid(row=0, column=2)


        #button frame
        btn_frame = Frame(class_frame, bd=0, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=255, width=778, height=100)

        # Buttons
        # save_btn = Button(btn_frame, command=self.add_data, text="Save", width=17, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        # save_btn.grid(row=0, column=0, padx=15, pady=10)

        update_btn = Button(btn_frame, command=self.update_data, text="Update", width=17, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        update_btn.place(x=135, y=0, width=500, height=30 )

        # delete_btn = Button(btn_frame, text="Delete", width=17, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        # delete_btn.grid(row=0, column=2, padx=15, pady=10)
        #
        # reset_btn = Button(btn_frame, text="Reset", width=17, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        # reset_btn.grid(row=0, column=3, padx=15, pady=10)
        #
        btn_frame1 = Frame(class_frame, bd=0, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=300, width=778, height=35)
        #
        take_photo_btn = Button(btn_frame1, command= self.generated_dataset,text="Take Photo Sample", width=38, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        take_photo_btn.grid(row=1, column=0, padx=15)
        #
        # update_photo_btn = Button(btn_frame1, text="Update Photo Sample", width=39, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        # update_photo_btn.grid(row=1, column=1, padx=15)

    # -------Functions----------
    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student_Details(self.new_window)

    def add_data(self):
        add_data_to_database(
            self.var_dep.get(),
            self.var_shift.get(),
            self.var_year.get(),
            self.var_std_id.get(),
            self.var_std_name.get(),
            self.var_gender.get(),
            self.var_std_email.get(),
            self.var_phone.get(),
            self.var_parent_email.get(),
            self.var_address.get(),
            self.var_radio1.get(),
            self.var_std_rno.get(),
            self.root
        )

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
    # update data

    def update_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_id.get() == "" or self.var_std_name.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                update = messagebox.askyesno("Update", "Do you want to update this Student Details", parent=self.root)
                if update > 0:
                    connection = get_database_connection()
                    my_cursor = connection.cursor()

                    sql_query = """
                                    UPDATE student 
                                    SET `student_rollno`=%s, `dep`=%s, `shift`=%s, `year`=%s, `name`=%s, `gender`=%s, `student_email`=%s, `phone`=%s, `parent_email`=%s, `address`=%s 
                                    WHERE `student_id`=%s
                                """
                    data = (
                        self.var_std_rno.get(),
                        self.var_dep.get(),
                        self.var_shift.get(),
                        self.var_year.get(),
                        self.var_std_name.get(),
                        self.var_gender.get(),
                        self.var_std_email.get(),
                        self.var_phone.get(),
                        self.var_parent_email.get(),
                        self.var_address.get(),
                        self.var_std_id.get(),
                    )
                    my_cursor.execute(sql_query, data)

                    connection.commit()
                    connection.close()

                    messagebox.showinfo("Success", "Student details successfully updated", parent=self.root)
                    self.root.destroy()
                else:
                    return
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    #reset fields
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


    def generated_dataset(self):
        generate_dataset(self)







if __name__ == "__main__":
    root = Tk()
    obj = Update_Student(root)
    root.mainloop()