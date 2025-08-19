import pickle
import numpy as np
import face_recognition
import os
import cv2
import csv
import tkinter as tk
from tkinter import messagebox

# Directory paths
data_dir = 'StudentData'
image_dir = os.path.join(data_dir, 'images')
csv_file = os.path.join(data_dir, 'students.csv')
encoding_file = 'encodings.pkl'

# Create directories if they don't exist
os.makedirs(image_dir, exist_ok=True)

# Initialize CSV file with headers if it doesn't exist
# if not os.path.isfile(csv_file):
#     with open(csv_file, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['StudentID', 'StudentName', 'ImagePath'])
#
# # Function to capture an image manually
# def capture_image(student_id, name):
#     student_dir = os.path.join(image_dir, f"{student_id}_{name}")
#     os.makedirs(student_dir, exist_ok=True)
#
#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use default camera
#
#     if not cap.isOpened():
#         messagebox.showerror("Error", "Could not open camera!")
#         return
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             messagebox.showerror("Error", "Failed to capture image!")
#             break
#
#         cv2.putText(frame, "Press 'C' to Capture, 'Q' to Quit", (50, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#
#         cv2.imshow('Capture Image', frame)
#         key = cv2.waitKey(1) & 0xFF
#
#         if key == ord('c'):  # Press 'C' to capture
#             img_path = os.path.join(student_dir, "image.jpg")
#             cv2.imwrite(img_path, frame)
#
#             messagebox.showinfo("Success", f"Image captured successfully for {name}!")
#             cap.release()
#             cv2.destroyAllWindows()
#
#             # Save student details to CSV with ID and Name separated
#             with open(csv_file, 'a', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow([student_id, name, img_path])
#             return
#
#         elif key == ord('q'):  # Press 'Q' to quit
#             cap.release()
#             cv2.destroyAllWindows()
#             return
#
# # GUI for data entry
# def submit():
#     student_id = entry_id.get().strip()
#     name = entry_name.get().strip()
#
#     if student_id and name:
#         capture_image(student_id, name)
#     else:
#         messagebox.showwarning("Input Error", "Please enter both Student ID and Name.")
#
# # Setting up the GUI
# root = tk.Tk()
# root.title("Student Registration")
# root.geometry("500x300")  # Adjusted window size
#
# tk.Label(root, text="Student ID").pack(pady=5)
# entry_id = tk.Entry(root)
# entry_id.pack(pady=5)
#
# tk.Label(root, text="Student Name").pack(pady=5)
# entry_name = tk.Entry(root)
# entry_name.pack(pady=5)
#
# tk.Button(root, text="Submit", command=submit).pack(pady=10)
# tk.Button(root, text="Exit", command=root.destroy).pack(pady=5)
#
# root.mainloop()

# ==========================
# Face Encoding Process
# ==========================

# Load existing encodings if the file exists
if os.path.exists(encoding_file):
    with open(encoding_file, 'rb') as f:
        encoding_data = pickle.load(f)
        known_encodings = encoding_data['encodings']
        known_names = encoding_data['names']
else:
    known_encodings = []
    known_names = []

IMAGE_DIR = 'StudentData/images/'

# Keep track of already encoded students
existing_students = {tuple(name) for name in known_names}  # Convert list to set for quick lookup

for student_dir in os.listdir(IMAGE_DIR):
    student_path = os.path.join(IMAGE_DIR, student_dir)
    if not os.path.isdir(student_path):
        continue

    # Extract Student ID and Name separately
    if '_' not in student_dir:
        print(f"Skipping invalid directory format: {student_dir}")
        continue

    student_id, student_name = student_dir.split('_', 1)

    # Skip already encoded students
    if (student_id, student_name) in existing_students:
        print(f"Skipping already encoded student: {student_name} ({student_id})")
        continue

    for image_name in os.listdir(student_path):
        image_path = os.path.join(student_path, image_name)
        print(f"Processing {image_path} for {student_name}...")

        image = face_recognition.load_image_file(image_path)

        if image is None:
            print(f"Error: Could not load image {image_path}. Skipping...")
            continue

        face_locations = face_recognition.face_locations(image, model='hog')

        if not face_locations:
            print(f"No faces found in {image_path}. Skipping...")
            continue

        face_encodings = face_recognition.face_encodings(image, face_locations)

        for face_encoding in face_encodings:
            known_encodings.append(face_encoding)
            known_names.append([student_id, student_name])  # Store separately

# Serialize only new encodings without reprocessing old ones
encoding_data = {'encodings': known_encodings, 'names': known_names}

with open(encoding_file, 'wb') as f:
    pickle.dump(encoding_data, f)

print("Face encodings have been successfully saved to 'encodings.pkl'.")
