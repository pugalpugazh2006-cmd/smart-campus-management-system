-- Dummy Data for Smart Campus System

-- Users (admin, faculty, student)
-- Passwords should be hashed in real app. Here we use plain text as per app.py logic for demo.
INSERT INTO users (username, password_hash, role) VALUES 
('admin', 'admin123', 'admin'),
('faculty1', 'pass', 'faculty'),
('faculty2', 'pass', 'faculty'),
('student1', 'pass', 'student'),
('student2', 'pass', 'student');

-- Faculty Details
INSERT INTO faculty (user_id, full_name, employee_id, email, department) VALUES
(2, 'Dr. Alice Smith', 'FAC001', 'alice@college.edu', 'Computer Science'),
(3, 'Prof. Bob Jones', 'FAC002', 'bob@college.edu', 'Mathematics');

-- Student Details
INSERT INTO students (user_id, full_name, roll_number, email, department, current_year) VALUES
(4, 'John Doe', 'CS101', 'john@student.edu', 'Computer Science', 4),
(5, 'Jane Roe', 'CS102', 'jane@student.edu', 'Computer Science', 4);

-- Courses
INSERT INTO courses (company_code, name, department, faculty_id) VALUES
('CS401', 'Advanced Web Dev', 'Computer Science', 1),
('CS402', 'Database Systems', 'Computer Science', 1),
('MA101', 'Calculus I', 'Mathematics', 2);

-- Events
INSERT INTO events (title, description, event_date, location, created_by) VALUES
('Tech Fest 2024', 'Annual technology festival.', '2024-12-15 10:00:00', 'Auditorium', 1),
('Career Fair', 'Meet top companies.', '2024-11-20 09:00:00', 'Campus Ground', 1);

-- Fees
INSERT INTO fees (student_id, title, amount_total, amount_paid, status) VALUES
(1, 'Semester 7 Tuition', 5000.00, 5000.00, 'Paid'),
(2, 'Semester 7 Tuition', 5000.00, 2000.00, 'Partial');
