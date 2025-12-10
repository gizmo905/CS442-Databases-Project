# backend/db_config.py
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Beenu2ashish",        
        database="college_db"
    )
    return conn
