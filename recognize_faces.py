import cv2
import face_recognition
import pickle
import pandas as pd
from datetime import datetime


# Load known encodings
def load_encodings(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data['encodings'], data['names']  # names stored as [Student_ID, Student_Name]


# Initialize attendance dataframe
def initialize_attendance(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Student_ID', 'Student_Name', 'Date', 'Time'])


# Mark attendance in CSV
def mark_attendance(student_id, student_name, attendance_df, file_path):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    # Check if the student has already been marked present today
    if not ((attendance_df['Student_ID'] == student_id) & (attendance_df['Date'] == date_str)).any():
        new_entry = pd.DataFrame(
            {'Student_ID': [student_id], 'Student_Name': [student_name], 'Date': [date_str], 'Time': [time_str]})
        attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)
        attendance_df.to_csv(file_path, index=False)
        print(f"✅ Attendance marked for {student_name} ({student_id}) at {time_str} on {date_str}.")
    else:
        print(f"⚠️ Attendance already marked for {student_name} ({student_id}) on {date_str}.")

    return attendance_df


# Main function
def main():
    encodings_file = 'encodings.pkl'
    attendance_file = 'attendance.csv'

    known_face_encodings, known_face_data = load_encodings(encodings_file)
    attendance_df = initialize_attendance(attendance_file)

    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce webcam buffer delay

    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    print("🎥 Starting video stream. Press 'q' to quit.")
    frame_counter = 0  # Process every 3rd frame for speed

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture image.")
                break

            frame_counter += 1
            if frame_counter % 3 != 0:  # Process every 3rd frame
                continue

            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)  # Resize for speed
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")  # Faster than CNN
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                name = "Unknown"
                student_id = "Unknown"

                if True in matches:
                    best_match_index = matches.index(True)
                    student_id, name = known_face_data[best_match_index]  # Retrieve Student_ID and Name separately
                    attendance_df = mark_attendance(student_id, name, attendance_df, attendance_file)

                # Scale back face location since we resized the frame
                top, right, bottom, left = face_location
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                # Draw rectangle & label
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, f"{student_id} - {name}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
