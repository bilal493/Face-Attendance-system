from tkinter import*
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Student.add_student import Add_Student
import os
import numpy as np
import cv2

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x890+0+0")
        self.root.title("Face Attendance System")

        # title
        title = Label(self.root, text="Train Dataset", font=("", 25, "bold"), bg="lightgoldenrod4", fg="white")
        title.place(x=0, y=20, width=1530, height=60)

        b1 = Button(text="Train Data", command=self.train_dataset, font=("", 15, "bold"), bg="lightgoldenrod3",
                    cursor="hand2", relief="groove")
        b1.place(x=1000, y=400, width=250, height=60)


    def train_dataset(self):
        data_dir = r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\Backend\Generate_Data\data"
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        # Check if the directory is empty
        if not path:
            messagebox.showerror("Error", "No data found to train!")
            return

        faces = []
        ids = []
        for image in path:

            gray_img = Image.open(image).convert("L")  # Convert to grayscale
            image_np = np.array(gray_img, "uint8")  # Convert to NumPy array
            id = int(os.path.split(image)[1].split(".")[1])  # Extract student ID

            faces.append(image_np)
            ids.append(id)  # Ensure IDs are integers
            cv2.imshow("Traning", image_np)
            cv2.waitKey(1) == 13
        ids = np.array(ids)

        classifier = cv2.face.LBPHFaceRecognizer_create()
        classifier.train(faces, ids)
        classifier.write(r"C:\Users\IT-LINKS\PycharmProjects\Attendence_System\Backend\Generate_Data\classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training dataset completed")





if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()