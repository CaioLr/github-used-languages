import os, psycopg2 # type: ignore
from dotenv import load_dotenv # type: ignore

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
            svg_light BYTEA,
            svg_dark BYTEA
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
    c.execute("SELECT svg_light, svg_dark FROM user_svg WHERE username = %s;",(username,))
    response = c.fetchone()
    conn.close()
    return response

def insert_user_svg(data: dict) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO user_svg (username,last_update,svg_light,svg_dark) VALUES (%s,%s,%s,%s)",(data['username'], data['last_update'], data['svg_light'], data['svg_dark']))
    conn.commit()
    conn.close()

def update_user_svg(data: dict) -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE user_svg SET last_update = %s, svg_light = %s, svg_dark = %s WHERE username = %s",(data['last_update'], data['svg_light'], data['svg_dark'], data['username']))
    conn.commit()
    conn.close()

def check_amount() -> None:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM user_svg")
    amount = c.fetchone()
    amount = int(amount[0])

    if amount >= 4500:
        c.execute("WITH first AS (SELECT id FROM user_svg ORDER BY id ASC LIMIT 1) DELETE FROM user_svg WHERE id IN (SELECT id FROM first)")
        conn.commit()

    conn.close()