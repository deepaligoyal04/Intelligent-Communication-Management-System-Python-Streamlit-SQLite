import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "communication_requests.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT, email TEXT, subject TEXT NOT NULL, message TEXT NOT NULL,
            category TEXT, priority TEXT, department TEXT, suggested_response TEXT,
            status TEXT DEFAULT 'Pending', created_at TEXT, updated_at TEXT
        )
        """)

def add_request(sender, email, subject, message, category, priority, department, suggested_response):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as con:
        cur = con.execute("""INSERT INTO requests
        (sender,email,subject,message,category,priority,department,suggested_response,status,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (sender,email,subject,message,category,priority,department,suggested_response,"Pending",now,now))
        return cur.lastrowid

def get_requests():
    with get_connection() as con:
        return pd.read_sql_query("SELECT * FROM requests ORDER BY id DESC", con)

def update_status(request_id, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as con:
        con.execute("UPDATE requests SET status=?, updated_at=? WHERE id=?", (status, now, request_id))

def delete_request(request_id):
    with get_connection() as con:
        con.execute("DELETE FROM requests WHERE id=?", (request_id,))
