import sqlite3
from datetime import datetime, timezone

def init_db() -> None:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_svg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            last_update NUMERIC,
            svg BLOB
        )
    ''')
    conn.commit()
    conn.close()

def get_user_last_update(username: str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT last_update FROM user_svg WHERE username = ?;",(username,))
    response = c.fetchone()
    conn.close()
    return response

def get_user_svg(username: str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT svg FROM user_svg WHERE username = ?;",(username,))
    response = c.fetchone()
    conn.close()
    return response

def insert_user_svg(data: dict) -> None:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_svg (username,last_update,svg) VALUES (?,?,?)",(data['username'], data['last_update'], data['svg']))
    conn.commit()
    conn.close()

def update_user_svg(data: dict) -> None:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE user_svg SET last_update = ?, svg = ? WHERE username = ?",(data['last_update'], data['svg'], data['username']))
    conn.commit()
    conn.close()

def check_amount() -> None:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM user_svg")
    amount = c.fetchone()
    amount = int(amount[0])

    if amount >= 200:
        c.execute("WITH first AS (SELECT id FROM user_svg ORDER BY id ASC LIMIT 1) DELETE FROM user_svg WHERE id IN (SELECT id FROM first)")
        conn.commit()

    conn.close()