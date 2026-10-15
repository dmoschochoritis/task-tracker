from player import decide


def test_null_playlist_shows_placeholder():
    assert decide(200, None) == "No content assigned"


def test_unknown_screen_shows_error():
    assert decide(404, {"detail": "Screen not found"}) == "Unknown screen"


def test_assigned_playlist_shows_name_and_items():
    body = {"id": 1, "name": "Morning", "items": ["a.png", "b.png"]}
    assert decide(200, body) == "Playing Morning: a.png, b.png"
