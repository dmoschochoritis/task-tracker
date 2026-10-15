from player import decide


def test_null_playlist_shows_placeholder():
    assert decide(200, None) == "No content assigned"


def test_unknown_screen_shows_error():
    assert decide(404, {"detail": "Screen not found"}) == "Unknown screen"


def test_assigned_playlist_shows_name_and_items():
    body = {"id": 1, "name": "Morning", "items": ["a.png", "b.png"]}
    assert decide(200, body) == "Playing Morning: a.png, b.png"

import urllib.error
import player
import logging


def test_offline_keeps_last_playlist(monkeypatch, caplog):
    def broken_fetch(screen_id):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(player, "fetch", broken_fetch)
    assert player.poll(1, "Playing Morning: a.png") == "Playing Morning: a.png"
    assert "unreachable" in caplog.text

def test_recovery_is_logged(monkeypatch, caplog):
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(player, "offline", False)

    def broken_fetch(screen_id):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr(player, "fetch", broken_fetch)
    player.poll(1, "Playing Morning: a.png")

    monkeypatch.setattr(player, "fetch", lambda screen_id: (200, None))
    player.poll(1, "Playing Morning: a.png")

    assert "reachable again" in caplog.text
