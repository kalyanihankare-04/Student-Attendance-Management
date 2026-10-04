from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Add Student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll_no = request.form["roll_no"]
        course = request.form["course"]

        conn = get_db()

        conn.execute(
            "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
            (name, roll_no, course)
        )

        conn.commit()
        conn.close()

        return redirect("/students")

    return render_template("add_student.html")


# View Students
@app.route("/students")
def students():

    conn = get_db()

    data = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=data
    )


# Mark Attendance
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    conn = get_db()

    if request.method == "POST":

        student_id = request.form["student_id"]
        status = request.form["status"]

        conn.execute(
            "INSERT INTO attendance (student_id, status) VALUES (?, ?)",
            (student_id, status)
        )

        conn.commit()

    students_data = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "attendance.html",
        students=students_data
    )


# Attendance Report
@app.route("/report")
def report():

    conn = get_db()

    records = conn.execute("""
        SELECT students.name,
               students.roll_no,
               students.course,
               attendance.status,
               attendance.date
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        ORDER BY attendance.date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "report.html",
        records=records
    )


# Create Database Tables
if __name__ == "__main__":

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            status TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()

    app.run(debug=True)