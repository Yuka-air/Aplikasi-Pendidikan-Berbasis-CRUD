# database.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # ganti sesuai konfigurasi MySQL kamu
        password="",          # isi kalau ada password
        database="db_2310010507"
    )
