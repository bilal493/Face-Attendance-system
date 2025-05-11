from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from Backend.Controller.fetch_data_controller import fetch_student_data
from tkinter import messagebox
from Backend.Database.db_connection import get_database_connection
import os
import csv
from tkinter import filedialog

my_data = []
class Developer:
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
        title = Label(self.root, text="Developer", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)

        main_frame = Frame(bg, bd=5, bg="")
        main_frame.place(x=1000, y=90, width=500, height=600)

        search_label = Label(main_frame, text="Hello My name is Bilal", font=("", 20, "bold"), bg="white")
        search_label.place(x= 0, y=5)

        search_label = Label(main_frame, text="I am a Full Stack Developer", font=("", 15, "bold"), bg="white")
        search_label.place(x=0, y=40)


if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()