# Smart Campus Management System

## Abstract
The **Smart Campus Management System** is a comprehensive web-based application designed to streamline and automate the administrative and academic processes of an educational institution. By integrating modules for attendance, fee management, event registration, and student performance tracking into a single unified platform, this project aims to enhance efficiency, reduce manual workload, and provide real-time insights to students, faculty, and administrators.

## Objectives
1.  **Digitize Campus Operations**: To replace manual record-keeping with a centralized digital database.
2.  **Enhance Accessibility**: To provide students and faculty with 24/7 access to academic records and administrative services.
3.  **Improve Transparency**: To ensure parents and students have clear visibility into attendance and financial status.
4.  **Simplify Management**: To offer administrators a powerful tool for managing users, events, and academic resources.
5.  **Role-Based Security**: To implement secure access control ensuring data privacy for different user roles.

## System Requirements
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js)
- **Backend**: Python 3.x, Flask Framework
- **Database**: MySQL

## Setup Instructions

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Database Setup**:
    - Ensure MySQL is running.
    - Create a database named `smartcampus`.
    - Run the schema script to create tables:
      ```sh
      mysql -u root -p smartcampus < schema.sql
      ```
    - (Optional) Populate with dummy data:
      ```sh
      mysql -u root -p smartcampus < dummy_data.sql
      ```
    - **Easier Method**: Run the python initialization script (ensures DB exists):
      ```bash
      python init_db.py
      ```

3.  **Configuration**:
    - Update `config.py` or create a `.env` file with your MySQL credentials.

4.  **Run Application**:
    ```bash
    python app.py
    ```
    - Access the app at `http://127.0.0.1:5000`

## Conclusion
The Smart Campus Management System successfully demonstrates the application of modern web technologies to solve real-world problems in educational administration. The modular architecture allows for easy scalability, making it a solid foundation for future enhancements such as mobile app integration or AI-based performance analytics. This project serves as a practical implementation of Full Stack Development concepts suitable for a final year college project.
