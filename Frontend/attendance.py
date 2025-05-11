from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector
import csv
import os
from Backend.Database.db_connection import get_database_connection

class Attendance_Details:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x890+0+0")
        self.root.title("Face Attendance System")

        # Variables
        self.var_att_id = StringVar()
        self.var_att_rollno = StringVar()
        self.var_att_name = StringVar()
        self.var_att_dep = StringVar()
        self.var_att_time = StringVar()
        self.var_att_date = StringVar()
        self.var_att_attendance = StringVar()

        self.page_size = 10  # Number of records per page
        self.current_page = 1  # Track the current page
        self.total_pages = 1  # Total pages calculated dynamically

        # Background
        bg = Label(self.root, bg="floralwhite")
        bg.place(x=0, y=0, width=1530, height=890)

        # Title
        title = Label(self.root, text="Attendance Management", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)

        # Main Frame
        main_frame = Frame(bg, bd=5)
        main_frame.place(x=10, y=110, width=1500, height=900)

        title = Label(main_frame, text="Attendance Details", font=("", 15, "bold"), fg="white", bg="lightgoldenrod4")
        title.place(x=150, y=10, width=1200, height=30)

        # Search Frame
        search_frame = LabelFrame(main_frame, bd=1, bg="white", relief=RIDGE, text="Search System", font=("", 10))
        search_frame.place(x=150, y=55, width=1200, height=100)

        # Search by Date
        search_label = Label(search_frame, text="Search by Date (YYYY-MM-DD):", font=("", 11, "bold"), bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.search_entry = ttk.Entry(search_frame, textvariable=self.var_att_date, width=25, font=("", 11))
        self.search_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        search_btn = Button(search_frame, command=self.fetch_filtered_data, text="Search", width=12, font=("", 11, "bold"),
                            bg="lightgoldenrod4", fg="white")
        search_btn.grid(row=0, column=2, padx=5, sticky=W)

        reset_btn = Button(search_frame, command=self.reset_data, text="Reset", width=12, font=("", 11, "bold"),
                           bg="lightgoldenrod4", fg="white")
        reset_btn.grid(row=0, column=3, padx=5, sticky=W)

        # Table Frame
        table_frame = Frame(main_frame, bd=1, bg="white", relief=RIDGE)
        table_frame.place(x=175, y=180, width=1155, height=400)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReport_Table = ttk.Treeview(table_frame, columns=("id", "roll_no", "name", "department", "time", "date", "attendance"),
                                                   xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.AttendanceReport_Table.xview)
        scroll_y.config(command=self.AttendanceReport_Table.yview)

        self.AttendanceReport_Table.heading("id", text="Attendance ID")
        self.AttendanceReport_Table.heading("roll_no", text="Roll no")
        self.AttendanceReport_Table.heading("name", text="Name")
        self.AttendanceReport_Table.heading("department", text="Department")
        self.AttendanceReport_Table.heading("time", text="Time")
        self.AttendanceReport_Table.heading("date", text="Date")
        self.AttendanceReport_Table.heading("attendance", text="Attendance")

        self.AttendanceReport_Table["show"] = "headings"

        for col in ("id", "roll_no", "name", "department", "time", "date", "attendance"):
            self.AttendanceReport_Table.column(col, width=100)

        self.AttendanceReport_Table.pack(fill=BOTH, expand=1)

        # Pagination Buttons
        pagination_frame = Frame(main_frame, bd=1, bg="white", relief=RIDGE)
        pagination_frame.place(x=175, y=600, width=1155, height=50)

        self.prev_btn = Button(pagination_frame, text="Previous", command=self.previous_page, font=("", 11, "bold"),
                               bg="lightgoldenrod4", fg="white", width=12)
        self.prev_btn.pack(side=LEFT, padx=10, pady=10)

        self.page_label = Label(pagination_frame, text=f"Page {self.current_page} of {self.total_pages}",
                                font=("", 11, "bold"), bg="white")
        self.page_label.pack(side=LEFT, padx=10, pady=10)

        self.next_btn = Button(pagination_frame, text="Next", command=self.next_page, font=("", 11, "bold"),
                               bg="lightgoldenrod4", fg="white", width=12)
        self.next_btn.pack(side=LEFT, padx=10, pady=10)

        # Load initial data
        self.fetch_data()

    # ------- Database Functions --------
    def fetch_data(self):
        """ Fetch paginated attendance records """
        try:
            connection = get_database_connection()
            my_cursor = connection.cursor()

            # Get total count of records
            my_cursor.execute("SELECT COUNT(*) FROM attendance")
            total_records = my_cursor.fetchone()[0]
            self.total_pages = (total_records // self.page_size) + (1 if total_records % self.page_size != 0 else 0)

            offset = (self.current_page - 1) * self.page_size
            my_cursor.execute(f"SELECT * FROM attendance ORDER BY date DESC LIMIT {self.page_size} OFFSET {offset}")
            rows = my_cursor.fetchall()

            connection.close()
            self.update_table(rows)
        except Exception as e:
            print(f"Error in fetch_data: {e}")

    def fetch_filtered_data(self):
        """ Fetch records for a specific date """
        try:
            date = self.var_att_date.get()
            if not date:
                messagebox.showerror("Error", "Please enter a date!", parent=self.root)
                return

            connection = get_database_connection()
            my_cursor = connection.cursor()
            my_cursor.execute("SELECT * FROM attendance WHERE date = %s", (date,))
            rows = my_cursor.fetchall()
            connection.close()

            self.update_table(rows)
        except Exception as e:
            print(f"Error in fetch_filtered_data: {e}")

    def update_table(self, rows):
        """ Update UI table with given data """
        self.AttendanceReport_Table.delete(*self.AttendanceReport_Table.get_children())
        for row in rows:
            self.AttendanceReport_Table.insert("", END, values=row)
        self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")

    def next_page(self):
        """ Load next page of data """
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.fetch_data()

    def previous_page(self):
        """ Load previous page of data """
        if self.current_page > 1:
            self.current_page -= 1
            self.fetch_data()

    def reset_data(self):
        """ Reset filters and reload all data """
        self.var_att_date.set("")
        self.current_page = 1
        self.fetch_data()


if __name__ == "__main__":
    root = Tk()
    obj = Attendance_Details(root)
    root.mainloop()
