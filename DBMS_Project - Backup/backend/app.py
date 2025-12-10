# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
from datetime import date

app = Flask(__name__)
CORS(app)  # allow http://127.0.0.1:5500 etc.

# =========================================================
# 1) ADVISOR "ME" ENDPOINT
# =========================================================
@app.get("/api/advisor/me")
def get_advisor_me():
    advisor_id = 1  # hard-coded for now
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT a.advisor_id, p.fname, p.lname, d.dept_name
        FROM advisor a
        JOIN person p ON a.email = p.email
        LEFT JOIN department d ON a.dept_id = d.dept_id
        WHERE a.advisor_id = %s
        """,
        (advisor_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"message": "Advisor not found"}), 404
    return jsonify(row)

# =========================================================
# 2) ADVISOR STUDENT SEARCH / CRUD
# =========================================================
@app.get("/api/students")
def search_students():
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify([])

    pattern = f"%{q}%"
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT s.student_id, s.major, s.gpa, p.fname, p.lname
        FROM student s
        JOIN person p ON s.email = p.email
        WHERE s.student_id LIKE %s
           OR p.fname LIKE %s
           OR p.lname LIKE %s
           OR s.major LIKE %s
        """,
        (pattern, pattern, pattern, pattern),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


# --- CREATE STUDENT ---
@app.post("/api/students")
def create_student():
    """
    Create a new student plus (if needed) a person row.
    Expected JSON body:
    {
        "fname": "...",         # required
        "lname": "...",         # required
        "email": "...",         # required
        "major": "...",         # optional
        "gpa": "3.45",          # optional, string or number
        "advisor_email": "advisor@univ.edu"  # required for now
    }
    """
    data = request.get_json() or {}

    fname = (data.get("fname") or "").strip()
    lname = (data.get("lname") or "").strip()
    email = (data.get("email") or "").strip()
    major = (data.get("major") or "").strip() or None
    advisor_email = (data.get("advisor_email") or "").strip()
    gpa_raw = data.get("gpa")

    if not fname or not lname or not email:
        return (
            jsonify(
                {"message": "First name, last name, and email are required."}
            ),
            400,
        )

    # Parse GPA if provided
    gpa = None
    if gpa_raw not in (None, ""):
        try:
            gpa = float(gpa_raw)
        except ValueError:
            return jsonify({"message": "GPA must be a number."}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Look up advisor_id from advisor_email (if provided)
    advisor_id = None
    if advisor_email:
        cur.execute(
            "SELECT advisor_id FROM advisor WHERE email = %s",
            (advisor_email,),
        )
        adv = cur.fetchone()
        if not adv:
            cur.close()
            conn.close()
            return jsonify({"message": "Advisor not found for email."}), 400
        advisor_id = adv["advisor_id"]

    # Ensure person row exists
    cur.execute("SELECT email FROM person WHERE email = %s", (email,))
    existing = cur.fetchone()
    if not existing:
        cur.execute(
            "INSERT INTO person (email, fname, lname) VALUES (%s, %s, %s)",
            (email, fname, lname),
        )

    # Compute entry_year and graduation_date
    today = date.today()
    entry_year = today.year
    grad_date = date(today.year + 3, today.month, today.day)

    # Insert student row
    cur.execute(
        """
        INSERT INTO student (
            email, advisor_id, major, gpa, graduation_date, entry_year
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (email, advisor_id, major, gpa, grad_date, entry_year),
    )
    student_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()

    return (
        jsonify(
            {
                "student_id": student_id,
                "email": email,
                "fname": fname,
                "lname": lname,
                "major": major,
                "gpa": gpa,
                "advisor_id": advisor_id,
                "entry_year": entry_year,
                "graduation_date": grad_date.isoformat(),
            }
        ),
        201,
    )


# --- UPDATE STUDENT ---
@app.put("/api/students/<int:student_id>")
def update_student(student_id):
    data = request.get_json() or {}
    major = (data.get("major") or "").strip() or None
    gpa_raw = data.get("gpa")

    gpa = None
    if gpa_raw not in (None, ""):
        try:
            gpa = float(gpa_raw)
        except ValueError:
            return jsonify({"message": "GPA must be a number."}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE student SET major = %s, gpa = %s WHERE student_id = %s",
        (major, gpa, student_id),
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Student updated successfully."})


# --- DELETE STUDENT ---
@app.delete("/api/students/<int:student_id>")
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student deleted successfully."})

# =========================================================
# 3) ADVISOR QUICK REPORTS
# =========================================================

# 3.1 Low GPA CS first-year
@app.get("/api/reports/low-gpa")
def report_low_gpa():
    """Low-GPA first-year CS students, ordered by GPA, plus cohort average."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT 
            s.student_id,
            p.fname,
            p.lname,
            s.major,
            s.gpa,
            s.entry_year,
            (
                SELECT AVG(s2.gpa)
                FROM student s2
                WHERE s2.major = 'Computer Science'
                  AND s2.entry_year = s.entry_year
                  AND s2.gpa IS NOT NULL
            ) AS cohort_avg_gpa
        FROM student s
        JOIN person p ON s.email = p.email
        WHERE s.major = 'Computer Science'
          AND s.gpa < 2.5
          AND s.entry_year = 2025
        ORDER BY s.gpa ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


# 3.2 MATH 164 Fall 2025 ≥ 95% capacity
@app.get("/api/reports/high-capacity")
def report_high_capacity():
    """MATH 164 sections in Fall 2025 at or above 95% capacity."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT
            c.course_code,
            se.section_id,
            se.section_number,
            t.term_name,
            se.capacity,
            COUNT(sts.student_id) AS enrolled,
            (COUNT(sts.student_id) / se.capacity) * 100 AS percent_full
        FROM section se
        JOIN course c ON se.course_id = c.course_id
        JOIN term t ON se.term_id = t.term_id
        LEFT JOIN student_takes_section sts ON se.section_id = sts.section_id
        WHERE c.course_code = 'MATH 164'
          AND t.term_name = 'Fall 2025'
        GROUP BY
            c.course_code,
            se.section_id,
            se.section_number,
            t.term_name,
            se.capacity
        HAVING percent_full >= 95
        ORDER BY percent_full DESC, se.section_number ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


# 3.3 Instructor load
@app.get("/api/reports/instructor-load")
def report_instructor_load():
    """Instructor teaching load for Fall 2025."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT 
            i.instr_id,
            CONCAT(p.fname, ' ', p.lname) AS instructor_name,
            t.term_name,
            COUNT(DISTINCT se.section_id) AS sections_taught,
            SUM(c.credits * COALESCE(sts_cnt.enrolled, 0)) AS total_enrolled_credit_hours
        FROM instructor i
        JOIN person p ON i.email = p.email
        JOIN section se ON i.instr_id = se.instr_id
        JOIN term t ON se.term_id = t.term_id
        JOIN course c ON se.course_id = c.course_id
        LEFT JOIN (
            SELECT section_id, COUNT(*) AS enrolled
            FROM student_takes_section
            GROUP BY section_id
        ) AS sts_cnt ON se.section_id = sts_cnt.section_id
        WHERE t.term_name = 'Fall 2025'
        GROUP BY i.instr_id, instructor_name, t.term_name
        ORDER BY total_enrolled_credit_hours DESC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


# 3.4 Advisee count per advisor
@app.get("/api/reports/advisee-count")
def report_advisee_count():
    """Number of advisees per advisor."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT 
            a.advisor_id,
            CONCAT(p.fname, ' ', p.lname) AS advisor_name,
            COUNT(s.student_id) AS advisee_count
        FROM advisor a
        JOIN person p ON a.email = p.email
        LEFT JOIN student s ON s.advisor_id = a.advisor_id
        GROUP BY a.advisor_id, advisor_name
        HAVING advisee_count > 0
        ORDER BY advisee_count DESC, advisor_name ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


# 3.5 Average GPA by major
@app.get("/api/reports/avg-gpa-major")
def report_avg_gpa_by_major():
    """Average GPA per major."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT 
            s.major,
            COUNT(*) AS student_count,
            AVG(s.gpa) AS avg_gpa
        FROM student s
        WHERE s.gpa IS NOT NULL
        GROUP BY s.major
        HAVING student_count >= 1
        ORDER BY avg_gpa DESC, s.major ASC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

# =========================================================
# 4) STUDENT DASHBOARD - PROFILE & ENROLLMENTS
# =========================================================

@app.get("/api/student/me")
def get_student_me():
    """
    Return the profile of the logged-in student, looked up by email.
    Frontend calls: GET /api/student/me?email=<email>
    """
    email = (request.args.get("email") or "").strip()
    if not email:
        return jsonify({"message": "Missing email query parameter"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            s.student_id,
            p.fname,
            p.lname,
            s.major,
            s.gpa,
            a.advisor_id,
            ap.fname AS advisor_fname,
            ap.lname AS advisor_lname
        FROM student s
        JOIN person p ON s.email = p.email
        LEFT JOIN advisor a ON s.advisor_id = a.advisor_id
        LEFT JOIN person ap ON a.email = ap.email
        WHERE s.email = %s
        """,
        (email,),
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Student not found"}), 404

    advisor_name = None
    if row.get("advisor_fname"):
        advisor_name = f"{row['advisor_fname']} {row['advisor_lname']}"

    return jsonify(
        {
            "student_id": row["student_id"],
            "fname": row["fname"],
            "lname": row["lname"],
            "major": row["major"],
            "gpa": row["gpa"],
            "advisor_name": advisor_name,
        }
    )


@app.get("/api/student/courses")
def get_student_courses():
    """
    Return all sections for the logged-in student, looked up by email.
    Frontend calls: GET /api/student/courses?email=<email>
    """
    email = (request.args.get("email") or "").strip()
    if not email:
        return jsonify({"message": "Missing email query parameter"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # First find the student_id
    cur.execute(
        "SELECT student_id FROM student WHERE email = %s",
        (email,),
    )
    stu = cur.fetchone()
    if not stu:
        cur.close()
        conn.close()
        return jsonify({"message": "Student not found"}), 404

    student_id = stu["student_id"]

    # Now get the enrollments
    cur.execute(
        """
        SELECT
            c.course_code,
            c.course_title,
            se.section_number,
            t.term_name,
            se.capacity,
            inst.instr_id,
            ip.fname AS instr_fname,
            ip.lname AS instr_lname,
            se.section_id
        FROM student_takes_section sts
        JOIN section se ON sts.section_id = se.section_id
        JOIN course c ON se.course_id = c.course_id
        JOIN term t ON se.term_id = t.term_id
        LEFT JOIN instructor inst ON se.instr_id = inst.instr_id
        LEFT JOIN person ip ON inst.email = ip.email
        JOIN student s ON sts.student_id = s.student_id
        WHERE s.email = %s
        """,
        (email,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.post("/api/student/courses")
def add_student_course():
    """
    Add a new enrollment for the logged-in student.
    Frontend calls:
      POST /api/student/courses?email=<email>
    JSON body:
    {
        "course_code": "MATH 164" or "MATH164",
        "section_number": "1" or "001",
        "term_name": "Fall 2025"
    }
    """
    email = (request.args.get("email") or "").strip()
    if not email:
        return jsonify({"message": "Missing email query parameter"}), 400

    data = request.get_json() or {}

    raw_course_code = (data.get("course_code") or "").strip()
    course_code = raw_course_code.replace(" ", "").upper()

    raw_section = (str(data.get("section_number") or "")).strip()
    if not raw_section:
        return jsonify({"message": "section_number is required."}), 400
    try:
        section_number = f"{int(raw_section):03d}"
    except ValueError:
        return jsonify({"message": "section_number must be a number."}), 400

    term_name = (data.get("term_name") or "").strip()
    if not course_code or not term_name:
        return jsonify(
            {"message": "course_code and term_name are required."}
        ), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Find student_id for email
    cur.execute(
        "SELECT student_id FROM student WHERE email = %s",
        (email,),
    )
    stu = cur.fetchone()
    if not stu:
        cur.close()
        conn.close()
        return jsonify({"message": "Student not found"}), 404

    student_id = stu["student_id"]

    # Find matching section
    cur.execute(
        """
        SELECT
            se.section_id,
            c.course_code,
            c.course_title,
            se.section_number,
            t.term_name,
            se.capacity,
            inst.instr_id,
            ip.fname AS instr_fname,
            ip.lname AS instr_lname
        FROM section se
        JOIN course c ON se.course_id = c.course_id
        JOIN term t ON se.term_id = t.term_id
        LEFT JOIN instructor inst ON se.instr_id = inst.instr_id
        LEFT JOIN person ip ON inst.email = ip.email
        WHERE REPLACE(c.course_code, ' ', '') = %s
          AND se.section_number = %s
          AND TRIM(t.term_name) = TRIM(%s)
        """,
        (course_code, section_number, term_name),
    )
    sec = cur.fetchone()

    if not sec:
        cur.close()
        conn.close()
        return jsonify(
            {
                "message": (
                    "Section not found. Please check course code, "
                    "section number, and term name."
                )
            }
        ), 404

    section_id = sec["section_id"]

    # Prevent duplicate enrollment
    cur.execute(
        """
        SELECT *
        FROM student_takes_section
        WHERE student_id = %s AND section_id = %s
        """,
        (student_id, section_id),
    )
    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        return jsonify(
            {"message": "You are already enrolled in this section."}
        ), 400

    # Insert enrollment
    cur.execute(
        """
        INSERT INTO student_takes_section (student_id, section_id)
        VALUES (%s, %s)
        """,
        (student_id, section_id),
    )
    conn.commit()

    # Re-select row in same shape as GET /api/student/courses
    cur.execute(
        """
        SELECT
            c.course_code,
            c.course_title,
            se.section_number,
            t.term_name,
            se.capacity,
            inst.instr_id,
            ip.fname AS instr_fname,
            ip.lname AS instr_lname,
            se.section_id
        FROM student_takes_section sts
        JOIN section se ON sts.section_id = se.section_id
        JOIN course c ON se.course_id = c.course_id
        JOIN term t ON se.term_id = t.term_id
        LEFT JOIN instructor inst ON se.instr_id = inst.instr_id
        LEFT JOIN person ip ON inst.email = ip.email
        WHERE sts.student_id = %s AND sts.section_id = %s
        """,
        (student_id, section_id),
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        row = {
            "course_code": course_code,
            "course_title": sec.get("course_title"),
            "section_number": section_number,
            "term_name": term_name,
            "capacity": sec.get("capacity"),
            "instr_id": sec.get("instr_id"),
            "instr_fname": sec.get("instr_fname"),
            "instr_lname": sec.get("instr_lname"),
            "section_id": section_id,
        }

    return jsonify(row), 201


@app.delete("/api/student/courses/<int:section_id>")
def delete_student_course(section_id):
    """
    Drop a student's enrollment from a section.
    Frontend calls:
      DELETE /api/student/courses/<section_id>?email=<student_email>
    """
    email = (request.args.get("email") or "").strip()
    if not email:
        return jsonify({"message": "Missing email query parameter"}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Find student_id
    cur.execute("SELECT student_id FROM student WHERE email = %s", (email,))
    stu = cur.fetchone()
    if not stu:
        cur.close()
        conn.close()
        return jsonify({"message": "Student not found"}), 404

    student_id = stu["student_id"]

    # Delete enrollment row
    cur.execute(
        """
        DELETE FROM student_takes_section
        WHERE student_id = %s AND section_id = %s
        """,
        (student_id, section_id),
    )
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"message": "Enrollment dropped."})

# =========================================================
# 5) LOGIN ENDPOINT
# =========================================================
@app.post("/api/login")
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT 
            u.user_id,
            u.email,
            u.username,
            u.password_hash,
            u.role_id,
            u.is_active,
            r.role_name,
            p.fname,
            p.lname
        FROM users u
        LEFT JOIN person p ON u.email = p.email
        LEFT JOIN role r ON u.role_id = r.role_id
        WHERE u.email = %s
          AND u.password_hash = %s
          AND (u.is_active = 1 OR u.is_active IS NULL)
        """,
        (email, password),
    )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"message": "Invalid email or password."}), 401

    return jsonify(
        {
            "user_id": row["user_id"],
            "email": row["email"],
            "username": row["username"],
            "fname": row.get("fname"),
            "lname": row.get("lname"),
            "role": row.get("role_name"),  # e.g. 'student' or 'advisor'
        }
    )

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
