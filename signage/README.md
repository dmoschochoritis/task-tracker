# Mini Signage API

## Run locally
1. `cd signage`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`
4. Open `/docs` on port 8000

Data is stored in `signage.db`, created on first start (not committed).

## Endpoints
- `GET /screens` – list all screens
- `GET /screens/{id}` – one screen, 404 if unknown
- `POST /playlists` – create a playlist, returns 201
- `PUT /screens/{id}/playlist` – assign a playlist, 404 if screen or playlist unknown
- `GET /screens/{id}/playlist` – assigned playlist; `null` (200) if none assigned; 404 if screen unknown
- `GET /playlists` – list all playlists

## Run tests
1. `cd signage`
2. `pip install -r requirements-dev.txt`
3. `pytest`

## Run the dashboard
Needs two terminals, both starting from the repo root.

1. API:
```
   cd signage
   uvicorn main:app --reload
```
2. Dashboard:
```
   cd signage/dashboard
   python -m http.server 5500
```
3. Open port 5500 in the browser.

`DASHBOARD_ORIGIN` is the only address the API accepts browser calls from (CORS).
It defaults to `http://localhost:5500`, so locally you don't need to set it.

In Codespaces:
- start the API with your forwarded 5500 address, without a trailing `/`:
```
  DASHBOARD_ORIGIN=https://<codespace-name>-5500.app.github.dev uvicorn main:app --reload
```
- set port 8000 to Public, otherwise calls are redirected to GitHub sign-in and show as a CORS error

## Run the player
A third terminal, from the repo root:

```
cd signage
python player.py <screen-id>
```

The player checks the API every 10 seconds and prints the playlist when it changes.
It uses `SIGNAGE_API` (default `http://localhost:8000`) to find the API.

| API response        | Player shows                              |
|---------------------|-------------------------------------------|
| 200 + playlist      | `Playing <name>: <items>`                 |
| 200 + `null`        | `No content assigned`                     |
| 404                 | `Unknown screen`                          |
| API unreachable     | keeps last playlist, logs a warning       |
| API back            | logs `API reachable again`                |

## Architecture

```
Dashboard (browser) ──HTTP──▶ API (FastAPI) ──▶ SQLite (signage.db)
Player (Python)     ──HTTP──▶ API
```

- The API is the single source of truth. Dashboard and player never touch the database.
- Both dashboard and player depend on the API contract in Endpoints.
  A contract change must update both consumers (see SCRUM-33).
