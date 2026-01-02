from flask import Flask, request, jsonify
from db import get_db_connection
from flask import render_template
from flask import render_template
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Attendance System Backend Running"


@app.route('/faculty/login', methods=['POST'])
def faculty_login():
    data = request.json
    email = data['email']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM faculty WHERE email = %s",
        (email,)
    )
    faculty = cursor.fetchone()

    cursor.close()
    conn.close()

    if faculty:
        return jsonify({"message": "Login successful", "faculty": faculty})
    else:
        return jsonify({"message": "Invalid email"}), 401

@app.route('/attendance/mark', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data['student_id']
    subject_id = data['subject_id']
    date = data['date']
    status = data['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO attendance (student_id, subject_id, date, status) VALUES (%s, %s, %s, %s)",
        (student_id, subject_id, date, status)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Attendance marked successfully"})

@app.route('/attendance/<int:student_id>', methods=['GET'])
def get_attendance(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            sub.subject_name,
            ROUND(
                SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
                2
            ) AS attendance_percentage
        FROM attendance a
        JOIN subjects sub ON a.subject_id = sub.subject_id
        WHERE a.student_id = %s
        GROUP BY sub.subject_name
    """, (student_id,))

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/student')
def student_page():
    return render_template('student.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/faculty')
def faculty_page():
    return render_template('faculty.html')

if __name__ == '__main__':
    app.run(debug=True)