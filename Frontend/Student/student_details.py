from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from Backend.Controller.fetch_data_controller import fetch_student_data
from tkinter import messagebox
from Backend.Database.db_connection import get_database_connection

class Student_Details:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x890+0+0")
        self.root.title("Face Attendance System")
        self.var_std_id = StringVar()
        self.selected_student_data = None

        # background
        bg = Label(self.root, bg="floralwhite")
        bg.place(x=0, y=0, width=1530, height=890)

        # title
        title = Label(self.root, text="Student Management", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)

        # frame
        main_frame = Frame(bg, bd=5, bg="")
        main_frame.place(x=10, y=200, width=1500, height=600)

        title = Label(main_frame, text="Student Details", font=("", 15, "bold"), fg="white", bg="lightgoldenrod4")
        title.place(x=200, y=10, width=1100, height=30)

        # ---------Search System------------
        search_frame = LabelFrame(main_frame, bd=1, bg="white", relief=RIDGE, text="Search System",
                                 font=("", 10))
        search_frame.place(x=200, y=55, width=1100, height=540)

        # button frame
        button_frame = LabelFrame(search_frame, bd=0, bg="white", relief=RIDGE,
                                  font=("", 10))
        button_frame.place(x=10, y=0, width=920, height=90)

        search_label = Label(button_frame, text="Search by:", font=("", 11, "bold"), bg="white")
        search_label.grid(row=0, column=0, sticky=W)

        search_combo = ttk.Combobox(button_frame, font=("", 12, "bold"), state="readonly", width=20)
        search_combo["values"] = ("Select", "Roll #", "Phone Number")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=10, pady=10)

        option_label = Label(button_frame, text="Write selected Option:", font=("", 11, "bold"), bg="white")
        option_label.grid(row=1, column=0)

        search_entry = ttk.Entry(button_frame, width=25, font=("", 11))
        search_entry.grid(row=1, column=1, padx=10, sticky=W)

        search_btn = Button(button_frame, text="Search", width=15, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        search_btn.grid(row=1, column=2, padx=15)

        show_all_btn = Button(button_frame, text="Show All", width=15, font=("", 11, "bold"), bg="lightgoldenrod4", fg="white")
        show_all_btn.grid(row=0, column=2, padx=15)

        delete_btn = Button(button_frame, text="Delete", width=17, font=("", 11, "bold"), bg="lightgoldenrod4",
                            fg="white", command=self.delete_data)
        delete_btn.grid(row=0, column=3)

        update_btn = Button(button_frame, text="Update", width=17, font=("", 11, "bold"), bg="lightgoldenrod4",
                            fg="white", command=self.open_update_window)
        update_btn.grid(row=1, column=3)

        # Add Refresh Button
        refresh_btn = Button(button_frame, text="Refresh", width=17, font=("", 11, "bold"), bg="lightgoldenrod4",
                              fg="white", command=self.fetch_data)
        refresh_btn.grid(row=0, column=4, padx=15)

        # ---------table----------
        table_frame = Frame(main_frame, bd=1, bg="white", relief=RIDGE)
        table_frame.place(x=225, y=175, width=1050, height=400)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, columns=("dep", "shift", "year", "roll no", "id", "name", "gender", "student_email", "phone","parent_email", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("shift", text="Shift")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("roll no", text="Roll Number")
        self.student_table.heading("id", text="id")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("student_email", text="Student Email")
        self.student_table.heading("phone", text="Phone #")
        self.student_table.heading("parent_email", text="Parent's Email")
        self.student_table.heading("address", text="Address")

        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=100)
        self.student_table.column("shift", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("roll no", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("student_email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("parent_email", width=100)
        self.student_table.column("address", width=100)

        self.student_table.pack(fill= BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # -------Functions----------
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

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        self.selected_student_data = content["values"]
        if self.selected_student_data:  # Ensure a row is selected
            self.var_std_id.set(self.selected_student_data[4])


    def open_update_window(self):
        from Frontend.Student.update_student import Update_Student
        if not self.selected_student_data:
            messagebox.showerror("Error", "Please select a student to update!")
            return

        self.new_window = Toplevel(self.root)
        self.update_student_page = Update_Student(self.new_window, self.selected_student_data)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_update_window_close)

    def on_update_window_close(self):
        """Handles actions when the update window is closed."""
        try:
            self.new_window.destroy()  # Close the update window
            self.fetch_data()  # Reload the table data
        except Exception as e:
            messagebox.showerror("Error", f"Error while updating data: {str(e)}")

    # delete function
    def delete_data(self):
        if not self.selected_student_data:  # Check if a row is selected
            messagebox.showerror("Error", "Please select a student to delete!", parent=self.root)
            return

        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Student Deletion", "Do you want to delete this Student?",
                                             parent=self.root)
                if delete > 0:
                    connection = get_database_connection()
                    my_cursor = connection.cursor()

                    # Debug SQL query and value
                    sql = "DELETE FROM student WHERE student_id=%s"
                    val = (self.var_std_id.get(),)
                    print("DELETE Query:", sql, "Value:", val)

                    # Execute and commit
                    my_cursor.execute(sql, val)
                    connection.commit()
                    connection.close()

                    # Refresh data
                    self.fetch_data()

                    messagebox.showinfo("Delete", "Successfully deleted student details", parent=self.root)
                else:
                    return
            except Exception as es:
                print(f"Error in delete_data: {es}")
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student_Details(root)
    root.mainloop()
