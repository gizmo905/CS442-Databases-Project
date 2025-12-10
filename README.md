# College Advising Portal — DBMS Project  
A web-based application that allows **students** to view/edit enrollments and allows **advisors** to manage advisees and run reports.  
Built using **Flask + MySQL + HTML/CSS/JS**.

This README explains exactly how any new user can clone the repository and run the project locally.

---

#  1. Repository Contents:
backend/
  app.py
  db_config_example.py # template for database configuration
frontend/
  LoginPage.html
  StudentDashBoard.html
  advisor-dashboard.html
  login.css
  StudentDashBoard.css
  advisor-dashboard.css
sql/
  schema.sql # contains CREATE TABLE statements
  seed_data.sql # inserts sample users, students, advisors, sections, etc.
  
When you upload your current files to GitHub, ensure **folder names remain the same** so setup instructions work as-is.

---

# 2. Prerequisites

Anyone running the project must have:

- **Python 3.9+**
- **MySQL Server** (or MariaDB)
- **pip**
- **A modern web browser**
- *(Optional but recommended)* VS Code Live Server or Python’s built-in `http.server`

---

# 🚀 3. How to Run the Project (Step-by-Step)

This section is written for **ANY new user** — no prior knowledge of our code required.

---

## ✅ Step 1 — Clone the Repository

git clone https://github.com/gizmo905/CS442-Databases-Project.git
cd CS442-Databases-Project

## Step 2 — Set Up the MySQL Database

i.)Start MySQL.

ii.)Create the database:
        CREATE DATABASE college_db;
    
iii.)Run the schema:
        mysql -u root -p college_db < sql/schema.sql

iv.)Run the seed data:
        mysql -u root -p college_db < sql/seed_data.sql

## Step 3 — Configure the Backend Connection

Inside backend/, create your personal db_config.py:

    cd backend
    cp db_config_example.py db_config.py

Open db_config.py and update:
    conn = mysql.connector.connect(
              host="localhost",
              user="root",
              password="YOUR_MYSQL_PASSWORD",
              database="college_db"
    )

## Step 4 — Install Python Dependencies

Inside the backend/ folder:
    
    pip install flask flask-cors mysql-connector-python

If using a virtual environment:
    
    python -m venv venv
    venv/bin/activate    # macOS/Linux
    venv\Scripts\activate       # Windows
    pip install flask flask-cors mysql-connector-python

## Step 5 — Start the Backend Server

From inside the backend/ directory:
     
     python app.py

If successful, Flask will run at:
     
     http://127.0.0.1:5000

## Step 6 — Start the Frontend

Inside frontend/:
    
    python -m http.server 8000

Open:
    
    http://127.0.0.1:8000/LoginPage.html

## Step 7 — Log In and Start Using the App

# 📌 4. Important Notes for New Users
         i.)You NEVER need to edit HTML, CSS, or JS for setup
         
         ii.)You only edit ONE file: backend/db_config.py
         
         iii.)All endpoints already work
         
         iv.)If running backend on a different port
              Update the constant in all HTML files:
                   const API_BASE = "http://127.0.0.1:5000";
             But normally, no change is needed.
