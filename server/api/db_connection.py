import os, psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_svg (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            last_update TIMESTAMP WITH TIME ZONE,
            svg BYTEA
        )
    ''')
    conn.commit()
    conn.close()

def get_user_last_update(username: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT last_update FROM user_svg WHERE username = %s;",(username,))
    response = c.fetchone()
    conn.close()
    return response

def get_user_svg(username: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT svg FROM user_svg WHERE username = %s;",(username,))
    response = c.fetchone()
    conn.close()
    return response

def insert_user_svg(data: dict) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO user_svg (username,last_update,svg) VALUES (%s,%s,%s)",(data['username'], data['last_update'], data['svg']))
    conn.commit()
    conn.close()

def update_user_svg(data: dict) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE user_svg SET last_update = %s, svg = %s WHERE username = %s",(data['last_update'], data['svg'], data['username']))
    conn.commit()
    conn.close()

def check_amount() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM user_svg")
    amount = c.fetchone()
    amount = int(amount[0])

    if amount >= 7500:
        c.execute("WITH first AS (SELECT id FROM user_svg ORDER BY id ASC LIMIT 1) DELETE FROM user_svg WHERE id IN (SELECT id FROM first)")
        conn.commit()

    conn.close()