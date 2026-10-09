import sqlite3

DB_PATH = "signage.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, items TEXT NOT NULL)")
        conn.execute("CREATE TABLE IF NOT EXISTS assignments (screen_id INTEGER PRIMARY KEY, playlist_id INTEGER NOT NULL)")