# Mini Signage API

## Run locally
1. `cd signage`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`
4. Open `/docs` on port 8000

## Endpoints
- `GET /screens` – list all screens
- `GET /screens/{id}` – one screen, 404 if unknown
