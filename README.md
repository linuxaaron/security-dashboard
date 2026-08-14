# Security Dashboard

A full stack security monitoring dashboard built around FastAPI, SQLAlchemy, NVD vulnerability intelligence and a deterministic risk engine.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy + SQLite for development
- NVD CVE API 2.0
- TypeScript + Next.js
- Responsive dark security operations UI
- Pytest integration and unit tests
- Dockerfiles for backend and frontend

## Features

- Asset inventory
- CVE import and normalization
- CVSS and severity extraction
- Security event model
- Deterministic 0–100 security score
- Risk component breakdown
- Live dashboard refresh every 30 seconds
- Responsive asset and vulnerability tables

## Local development

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Dashboard: `http://localhost:3000`

Set `NEXT_PUBLIC_API_URL` if the API is running somewhere other than `http://127.0.0.1:8000`.

## Tests

```bash
cd backend
pytest -q
```

## Security notes

Secrets and local databases are excluded from Git. NVD API credentials, when used, must be supplied through environment variables and never committed to the repository.
