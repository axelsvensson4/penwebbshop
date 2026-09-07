# NORTHPOINT

En liten grund för en webbshop, utan produktinnehåll eller extra sidor.

- `frontend/pencil-webbshop`: Vue 3, Vite, Vuetify och Pinia.
- `backend`: FastAPI och SQLite.

## Starta backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Starta frontend

```powershell
cd frontend/pencil-webbshop
Copy-Item .env.example .env
npm install
npm run dev
```

Frontendens API-adress konfigureras med `VITE_API_BASE_URL` i `.env`.
