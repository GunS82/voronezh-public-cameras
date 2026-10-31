import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'cameras.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS cameras (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                player_url TEXT,
                operator TEXT,
                category TEXT,
                status TEXT,
                confidence TEXT,
                lat REAL,
                lng REAL,
                address TEXT,
                last_checked TEXT
            )
        ''')
    conn.close()

def save_camera(cam):
    conn = get_db()
    with conn:
        conn.execute('''
            INSERT OR REPLACE INTO cameras (
                id, title, url, player_url, operator, category, status, confidence, lat, lng, address, last_checked
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cam['id'], cam['title'], cam['url'], cam.get('player_url', ''), cam['operator'],
            cam['category'], cam['status'], cam['confidence'], cam.get('lat'), cam.get('lng'), cam.get('address'), cam.get('last_checked', '')
        ))
    conn.close()

def get_all_cameras():
    conn = get_db()
    cams = conn.execute('SELECT * FROM cameras').fetchall()
    conn.close()
    return [dict(cam) for cam in cams]

if __name__ == '__main__':
    init_db()
