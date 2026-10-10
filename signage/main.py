import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import get_connection, init_db

app = FastAPI(title="Mini Signage API")

init_db()

SCREENS = [
    {"id": 1, "name": "Lobby", "location": "Athens HQ"},
    {"id": 2, "name": "Cafe", "location": "Athens HQ"},
    {"id": 3, "name": "Window", "location": "Thessaloniki store"},
]

class PlaylistIn(BaseModel):
    name: str
    items: list[str]

class AssignIn(BaseModel):
    playlist_id: int

@app.get("/screens")
def list_screens():
    return SCREENS

@app.get("/screens/{screen_id}")
def get_screen(screen_id: int):
    for screen in SCREENS:
        if screen["id"] == screen_id:
            return screen
    raise HTTPException(status_code=404, detail="Screen not found")

@app.post("/playlists", status_code=200)
def create_playlist(playlist: PlaylistIn):
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO playlists (name, items) VALUES (?, ?)", (playlist.name, json.dumps(playlist.items)))
    return {"id": cur.lastrowid, "name": playlist.name, "items": playlist.items}

@app.put("/screens/{screen_id}/playlist")
def assign_playlist(screen_id: int, body: AssignIn):
    if not any(s["id"] == screen_id for s in SCREENS):
        raise HTTPException(status_code=404, detail="Screen not found")
    with get_connection() as conn:
        if conn.execute("SELECT id FROM playlists WHERE id = ?", (body.playlist_id,)).fetchone() is None:
            raise HTTPException(status_code=404, detail="Playlist not found")
        conn.execute("INSERT OR REPLACE INTO assignments (screen_id, playlist_id) VALUES (?, ?)", (screen_id, body.playlist_id))
    return {"screen_id": screen_id, "playlist_id": body.playlist_id}

@app.get("/screens/{screen_id}/playlist")
def get_screen_playlist(screen_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT p.id, p.name, p.items FROM assignments a JOIN playlists p ON p.id = a.playlist_id WHERE a.screen_id = ?", (screen_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No playlist assigned")
    return {"id": row["id"], "name": row["name"], "items": json.loads(row["items"])}
