from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mini Signage API")

SCREENS = [
    {"id": 1, "name": "Lobby", "location": "Athens HQ"},
    {"id": 2, "name": "Cafe", "location": "Athens HQ"},
    {"id": 3, "name": "Window", "location": "Thessaloniki store"},
]

@app.get("/screens")
def list_screens():
    return SCREENS

@app.get("/screens/{screen_id}")
def get_screen(screen_id: int):
    for screen in SCREENS:
        if screen["id"] == screen_id:
            return screen
    raise HTTPException(status_code=404, detail="Screen not found")
