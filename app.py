from flask import Flask, render_template, send_file
import pandas as pd
from io import BytesIO
from urllib.parse import quote as url_quote

app = Flask(__name__)

# ==========================
# Display Attendance
# ==========================a
@app.route('/')
def display_attendance():
    try:
        df = pd.read_csv('attendance.csv')  # Read attendance data
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Student_ID', 'Student_Name', 'Date', 'Time'])  # Default empty table

    # Clean DataFrame for proper formatting
    df = df.applymap(lambda x: str(x).strip(" ,'") if isinstance(x, str) else x)

    # Convert DataFrame to HTML table (Bootstrap-styled)
    attendance_table = df.to_html(index=False, classes='table table-bordered table-striped')

    return render_template('attendance.html', table=attendance_table)




# ==========================
# Download Attendance as Excel
# ==========================
@app.route('/download')
def download_attendance():
    try:
        df = pd.read_csv('attendance.csv')  # Read attendance data
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Student_ID', 'Student_Name', 'Date', 'Time'])  # Default empty table

    # Clean DataFrame for proper formatting
    df = df.applymap(lambda x: str(x).strip(" ,'") if isinstance(x, str) else x)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')

    output.seek(0)  # Move cursor back to start

    return send_file(output,
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                     download_name='attendance.xlsx',
                     as_attachment=True)


# ==========================
# Run Flask App
# ==========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
