import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Function to display attendance in Tkinter table
def display_attendance():
    try:
        df = pd.read_csv("attendance.csv")  # Load attendance data
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Student_ID", "Student_Name", "Date", "Time"])  # Empty table

    # Clear existing data in treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insert data into table
    if df.empty:
        messagebox.showinfo("No Records", "No attendance records found.")
    else:
        for _, row in df.iterrows():
            tree.insert("", "end", values=row.tolist())

# Function to download attendance as an Excel file in the Downloads folder
def download_attendance():
    try:
        df = pd.read_csv("attendance.csv")  # Load attendance data

        if df.empty:
            messagebox.showwarning("Download Failed", "No attendance data available to download.")
            return

        # Get the Downloads folder path
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_folder, "attendance.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Attendance")

        messagebox.showinfo("Download Successful", f"Attendance downloaded to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download attendance: {e}")

# Create main Tkinter window
root = tk.Tk()
root.title("Attendance Viewer")

# Set window size and center it
window_width, window_height = 650, 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# Header Label
tk.Label(root, text="📊 Attendance Records", font=("Arial", 16, "bold")).pack(pady=10)

# Create a table (Treeview) to display attendance
columns = ("Student_ID", "Student_Name", "Date", "Time")
tree = ttk.Treeview(root, columns=columns, show="headings")

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(pady=10, fill="both", expand=True)

# Buttons for functionalities
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🔄 Refresh Data", command=display_attendance, width=20).pack(side="left", padx=5)
tk.Button(btn_frame, text="📥 Download as Excel", command=download_attendance, width=20).pack(side="left", padx=5)

# Show data when the application opens
display_attendance()

root.mainloop()