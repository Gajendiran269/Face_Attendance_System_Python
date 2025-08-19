import os
import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to open Student Registration window
def open_register():
    try:
        subprocess.run(["python", "register.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open registration: {e}")

# Function to start face encoding
def open_encoding():
    try:
        subprocess.run(["python", "capture_student_data.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode faces: {e}")

# Function to take attendance
def open_attendance():
    try:
        subprocess.run(["python", "recognize_faces.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to take attendance: {e}")

# Function to open Attendance GUI
def open_attendance_details():
    try:
        subprocess.Popen(["python", "attendance_gui.py"])  # Open the new Tkinter attendance viewer
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open attendance viewer: {e}")

# Main GUI
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.attributes('-fullscreen', True)  # Enable fullscreen mode

# ===== HEADER (Moved Slightly Down) ===== #
header_frame = tk.Frame(root)
header_frame.pack(side="top", fill="x", pady=40)  # Moves the header slightly lower

tk.Label(header_frame, text="Mailam Engineering College", font=("Arial", 26, "bold"), anchor="center").pack()
tk.Label(header_frame, text="Information Technology", font=("Arial", 22), anchor="center").pack()

# ===== BUTTONS (Moved Slightly Up) ===== #
button_frame = tk.Frame(root)
button_frame.pack(pady=30)  # Moves buttons a little up

# Buttons for functionalities
tk.Button(button_frame, text="📷 Register Student", command=open_register, width=30, height=2, font=("Arial", 16)).pack(pady=10)
tk.Button(button_frame, text="🔍 Encode Faces", command=open_encoding, width=30, height=2, font=("Arial", 16)).pack(pady=10)
tk.Button(button_frame, text="📜 Take Attendance", command=open_attendance, width=30, height=2, font=("Arial", 16)).pack(pady=10)
tk.Button(button_frame, text="📊 View Attendance", command=open_attendance_details, width=30, height=2, font=("Arial", 16)).pack(pady=10)  # Updated button
tk.Button(button_frame, text="❌ Exit", command=root.quit, width=30, height=2, font=("Arial", 16), bg="red", fg="white").pack(pady=10)

# Exit fullscreen with "Esc" key
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)  # Press "Esc" to exit fullscreen

root.mainloop()
