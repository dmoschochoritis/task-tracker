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
- `GET /screens/{id}/playlist` – assigned playlist, 404 if none assigned

## Run tests
1. `cd signage`
2. `pip install -r requirements-dev.txt`
3. `pytest`
