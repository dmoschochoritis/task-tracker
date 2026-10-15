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
Needs two terminals.

1. API: `cd signage` then
   `DASHBOARD_ORIGIN=<dashboard address> uvicorn main:app --reload`
2. Dashboard: `cd signage/dashboard` then `python -m http.server 5500`
3. Open port 5500 in the browser.

`DASHBOARD_ORIGIN` is the only address the API accepts calls from (CORS).
Locally it defaults to `http://localhost:5500`.

In Codespaces:
- use the forwarded 5500 address, without a trailing `/`
- set port 8000 to Public, otherwise calls are redirected to GitHub sign-in and show as a CORS error
