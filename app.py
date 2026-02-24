from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from db import get_db_connection
import mysql.connector
from datetime import date, datetime

app = Flask(__name__)
app.config.from_object(Config)

# --- Authentication Routes ---

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        else:
            flash('Database connection failed', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    user_id = session['user_id']
    data = {}
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        if role == 'student':
            # Fetch student ID
            cursor.execute("SELECT * FROM students WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            if student:
                # Attendance summary
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_classes,
                        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present_classes
                    FROM attendance WHERE student_id = %s
                """, (student['id'],))
                att_stats = cursor.fetchone()
                if att_stats['total_classes'] > 0:
                    data['attendance_pct'] = round((att_stats['present_classes'] / att_stats['total_classes']) * 100, 2)
                else:
                    data['attendance_pct'] = 0
                
                # Pending Fees
                cursor.execute("SELECT SUM(amount_total - amount_paid) as pending FROM fees WHERE student_id = %s", (student['id'],))
                fee_stat = cursor.fetchone()
                data['pending_fees'] = fee_stat['pending'] or 0

                # Marks logic would go here
        
        elif role == 'faculty':
             cursor.execute("SELECT * FROM faculty WHERE user_id = %s", (user_id,))
             faculty = cursor.fetchone()
             if faculty:
                 # Count courses taught
                 cursor.execute("SELECT COUNT(*) as course_count FROM courses WHERE faculty_id = %s", (faculty['id'],))
                 data['course_count'] = cursor.fetchone()['course_count']

        elif role == 'admin':
            cursor.execute("SELECT COUNT(*) as count FROM students")
            data['student_count'] = cursor.fetchone()['count']
            cursor.execute("SELECT COUNT(*) as count FROM faculty")
            data['faculty_count'] = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
    
    return render_template('dashboard.html', role=role, username=session['username'], data=data)

# --- Attendance Routes ---

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    user_id = session['user_id']
    conn = get_db_connection()
    
    if role == 'faculty':
        if request.method == 'POST':
            # Marking attendance
            course_id = request.form['course_id']
            date_val = request.form['date']
            # Loop through student IDs from form
            # Assuming form sends student_ids and statuses
            
            # Simple implementation: expect a list of student_ids and a common status or individual
            # For this demo, let's assume we get lists.
            # However, standard form handling: separate keys.
            pass # See mark_attendance specific route

        # View Logic for Faculty: List courses to mark attendance
        courses = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.name 
                FROM courses c 
                JOIN faculty f ON c.faculty_id = f.id 
                WHERE f.user_id = %s
            """, (user_id,))
            courses = cursor.fetchall()
            cursor.close()
            conn.close()
        return render_template('attendance_faculty.html', courses=courses)

    elif role == 'student':
        # View own attendance
        attendance_records = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.name as course_name, a.date, a.status 
                FROM attendance a
                JOIN courses c ON a.course_id = c.id
                JOIN students s ON a.student_id = s.id
                WHERE s.user_id = %s
                ORDER BY a.date DESC
            """, (user_id,))
            attendance_records = cursor.fetchall()
            cursor.close()
            conn.close()
        return render_template('attendance_student.html', attendance=attendance_records)
    
    return redirect(url_for('dashboard'))

@app.route('/mark_attendance/<int:course_id>', methods=['GET', 'POST'])
def mark_attendance_route(course_id):
    # Check if faculty
    if 'role' not in session or session['role'] != 'faculty':
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    if request.method == 'POST':
        date_val = request.form['date']
        students = request.form.getlist('student_id')
        
        cursor = conn.cursor()
        for stud_id in students:
            status = request.form.get(f'status_{stud_id}')
            try:
                cursor.execute("""
                    INSERT INTO attendance (student_id, course_id, date, status)
                    VALUES (%s, %s, %s, %s)
                """, (stud_id, course_id, date_val, status))
            except mysql.connector.Error as err:
                 print(f"Error: {err}") # Likely duplicate entry
        conn.commit()
        cursor.close()
        conn.close()
        flash('Attendance marked successfully', 'success')
        return redirect(url_for('attendance'))

    # GET: Show list of students enrolled in this course (assuming all students in dept take it, or simple logic)
    # For this simplified DB, we didn't make a course_enrollment table.
    # We'll assume all students of the course's department are enrolled.
    students = []
    course = {}
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        course = cursor.fetchone()
        
        if course:
            cursor.execute("SELECT * FROM students WHERE department = %s", (course['department'],))
            students = cursor.fetchall()
            
        cursor.close()
        conn.close()
    
    return render_template('mark_attendance.html', course=course, students=students, today=date.today())

# --- Fee Routes ---

@app.route('/fees')
def fees():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    user_id = session['user_id']
    conn = get_db_connection()
    
    if role == 'student':
        fee_records = []
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.* 
                FROM fees f
                JOIN students s ON f.student_id = s.id
                WHERE s.user_id = %s
            """, (user_id,))
            fee_records = cursor.fetchall()
            cursor.close()
            conn.close()
        return render_template('fees_student.html', fees=fee_records)
    
    return redirect(url_for('dashboard'))

# --- Event Routes ---

@app.route('/events', methods=['GET', 'POST'])
def events():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    events_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events ORDER BY event_date DESC")
        events_list = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return render_template('events.html', events=events_list)

@app.route('/events/register/<int:event_id>', methods=['POST'])
def register_event(event_id):
    if session['role'] != 'student':
        flash('Only students can register', 'warning')
        return redirect(url_for('events'))
        
    user_id = session['user_id']
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM students WHERE user_id = %s", (user_id,))
        student = cursor.fetchone()
        
        if student:
            try:
                cursor.execute("INSERT INTO event_registrations (event_id, student_id) VALUES (%s, %s)", (event_id, student['id']))
                conn.commit()
                flash('Registered successfully!', 'success')
            except mysql.connector.Error:
                flash('Already registered or error.', 'info')
        
        cursor.close()
        conn.close()
    return redirect(url_for('events'))

# --- Admin Routes ---

@app.route('/admin/users')
def admin_users():
    if session.get('role') != 'admin':
         flash('Access denied', 'danger')
         return redirect(url_for('dashboard'))
         
    conn = get_db_connection()
    users = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, role, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('admin_users.html', users=users)

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if session.get('role') != 'admin':
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", (username, password, role))
                conn.commit()
                flash(f'User {username} created!', 'success')
            except mysql.connector.Error as err:
                flash(f'Error: {err}', 'danger')
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('admin_users'))
        
    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
