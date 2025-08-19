import os
import cv2
import csv
import tkinter as tk
from tkinter import messagebox

# Directory paths
data_dir = 'StudentData'
image_dir = os.path.join(data_dir, 'images')
csv_file = os.path.join(data_dir, 'students.csv')

# Ensure directories exist
os.makedirs(image_dir, exist_ok=True)

# Initialize CSV file if it doesn't exist
if not os.path.isfile(csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['StudentID', 'StudentName', 'ImagePath'])

# Capture student image
def capture_image(student_id, name):
    student_dir = os.path.join(image_dir, f"{student_id}_{name}")
    os.makedirs(student_dir, exist_ok=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Camera not accessible!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image!")
            break

        cv2.putText(frame, "Press 'C' to Capture, 'Q' to Quit", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Capture Image', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            img_path = os.path.join(student_dir, "image.jpg")
            cv2.imwrite(img_path, frame)
            cap.release()
            cv2.destroyAllWindows()

            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([student_id, name, img_path])

            messagebox.showinfo("Success", f"Image captured for {name}!")
            return

        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return

# GUI for Student Registration
def submit():
    student_id = entry_id.get().strip()
    name = entry_name.get().strip()

    if student_id and name:
        capture_image(student_id, name)
    else:
        messagebox.showwarning("Input Error", "Please enter Student ID and Name.")

root = tk.Tk()
root.title("Student Registration")
root.geometry("400x250")

tk.Label(root, text="Student ID").pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

tk.Label(root, text="Student Name").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

tk.Button(root, text="Submit", command=submit).pack(pady=10)
tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)

root.mainloop()
