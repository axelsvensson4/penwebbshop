# Backend

FastAPI-backend med SQLite. Databasfilen skapas automatiskt i `data/webshop.db` vid start.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API:t finns på `http://localhost:8000/api` och dokumentationen på `http://localhost:8000/docs`.

## API-status

Följande publika endpoints fungerar redan med den tomma SQLite-databasen:

- `GET /api/health`
- `GET /api/products` (stöder `category`, `outlet`, `available_only`, `limit`, `offset`)
- `GET /api/products/{product_id}`
- `GET /api/categories`
- `GET /api/faq`

Kundvagn, checkout, leverans, autentisering och konto har också dokumenterade endpoints i OpenAPI, men svarar med `501 Not Implemented`. De är avsiktliga integrationspunkter och ska kopplas till en vald autentiserings- respektive betallösning innan de aktiveras.
