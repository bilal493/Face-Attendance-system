import customtkinter as ctk
import tkinter.messagebox
import os
from Student.add_student import Add_Student
from Frontend.train import Train
from Frontend.recognition import Recognition
from Frontend.attendance import Attendance_Details
from time import strftime


class FaceAttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x800+100+50")
        self.root.title("Face Attendance System")

        # Set theme
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        # Background frame
        self.bg_frame = ctk.CTkFrame(self.root, fg_color="#F5F5F5")
        self.bg_frame.pack(fill="both", expand=True)

        # Navigation Bar
        self.navbar = ctk.CTkFrame(self.bg_frame, height=60, fg_color="#EAEAEA")
        self.navbar.pack(fill="x")

        self.title_label = ctk.CTkLabel(self.navbar, text="Face Attendance System", font=("Arial", 24, "bold"),
                                        text_color="#333")
        self.title_label.pack(side="left", padx=20)

        self.clock_label = ctk.CTkLabel(self.navbar, font=("Arial", 14, "bold"), text_color="#333")
        self.clock_label.pack(side="right", padx=20)
        self.update_time()

        # Main Content Area
        self.content_frame = ctk.CTkFrame(self.bg_frame, fg_color="#F5F5F5")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left side for photo
        self.photo_frame = ctk.CTkFrame(self.content_frame, width=700, fg_color="#FFFFFF", corner_radius=20)
        self.photo_frame.pack(side="left", fill="both", padx=20, pady=20, expand=True)

        self.photo_label = ctk.CTkLabel(self.photo_frame, text="Photo Placeholder", font=("Arial", 18, "bold"),
                                        text_color="#333")
        self.photo_label.pack(expand=True)

        # Right side for buttons
        self.button_frame = ctk.CTkFrame(self.content_frame, width=500, fg_color="#FFFFFF", corner_radius=20)
        self.button_frame.pack(side="right", fill="both", padx=40, pady=40)

        button_config = {
            "font": ("Arial", 16, "bold"),
            "height": 60,
            "width": 300,
            "fg_color": "#FFA500",
            "hover_color": "#FF8C00",
            "text_color": "black",
            "corner_radius": 15
        }

        button_data = [
            ("Student Details", self.student_details),
            ("Face Detector", self.recognize_data),
            ("Attendance", self.attendance),
            ("Train Data", self.train_data),
            ("Photos", self.open_img),
            ("Exit", self.exit)
        ]

        for text, command in button_data:
            button = ctk.CTkButton(self.button_frame, text=text, command=command, **button_config)
            button.pack(pady=15)

    def update_time(self):
        current_time = strftime('%H:%M:%S %p')
        self.clock_label.configure(text=current_time)
        self.clock_label.after(1000, self.update_time)

    def open_img(self):
        os.startfile(r"C:\\Users\\IT-LINKS\\PycharmProjects\\Attendence_System\\Backend\\Generate_Data\\data")

    def student_details(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = Add_Student(self.new_window)

    def train_data(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = Train(self.new_window)

    def recognize_data(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = Recognition(self.new_window)

    def attendance(self):
        self.new_window = ctk.CTkToplevel(self.root)
        self.app = Attendance_Details(self.new_window)

    def exit(self):
        exit_confirm = tkinter.messagebox.askyesno("Face Recognition", "Are you sure you want to exit?")
        if exit_confirm:
            self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = FaceAttendanceSystem(root)
    root.mainloop()
