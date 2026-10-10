import pytest
from fastapi.testclient import TestClient

import db
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "test.db"))
    db.init_db()
    return TestClient(app)

def test_create_playlist_returns_201(client):
    r = client.post("/playlists", json={"name": "Morning", "items": ["Hi"]})
    assert r.status_code == 201
    assert r.json()["id"] == 1


def test_assign_unknown_screen_returns_404(client):
    r = client.put("/screens/99/playlist", json={"playlist_id": 1})
    assert r.status_code == 404


def test_assign_and_read_back(client):
    client.post("/playlists", json={"name": "Morning", "items": ["Hi"]})
    client.put("/screens/1/playlist", json={"playlist_id": 1})
    r = client.get("/screens/1/playlist")
    assert r.json()["name"] == "Morning"
