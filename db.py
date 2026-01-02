import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Neethi@0301",
        database="attendance_system"
    )
