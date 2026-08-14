# Security Dashboard

A small security monitoring stack for keeping track of assets, CVEs and security events. The backend exposes a REST API and calculates a repeatable security score from the data in the database. The frontend turns that data into a dashboard that can be used locally or as a base for a larger security platform.

This is a portfolio project, but the code is structured like a real application rather than a static demo.

## What it does

The application currently covers four main areas:

1. Asset inventory
2. Vulnerability tracking
3. Security event tracking
4. Risk scoring

CVE data can be pulled from the NVD CVE API 2.0. Imported entries are normalized before they are stored in the database.

The dashboard reads the backend API and shows the current security score, risk level, assets, vulnerabilities and risk components. The frontend refreshes the dashboard data every 30 seconds.

## Tech stack

| Part | Technology |
| --- | --- |
| Frontend | Next.js 15, React 19, TypeScript |
| Backend | FastAPI, Uvicorn |
| Database | SQLite with SQLAlchemy |
| Vulnerability data | NVD CVE API 2.0 |
| Testing | pytest, FastAPI TestClient |
| Containers | Docker |
| CI | GitHub Actions |

## Project structure

```text
security-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   └── package.json
├── .github/
│   └── workflows/
├── docker-compose.yml
└── README.md
```

## Running it locally

### Backend

Python 3.13 is used for development.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is then available at:

```text
http://127.0.0.1:8000
```

Useful endpoints:

```text
GET  /health
GET  /api/v1
GET  /api/v1/assets
GET  /api/v1/vulnerabilities
GET  /api/v1/events
GET  /api/v1/dashboard/summary
POST /api/v1/vulnerabilities/import/{cve_id}
```

Example CVE import:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/vulnerabilities/import/CVE-2026-53647
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The dashboard runs at:

```text
http://localhost:3000
```

By default the frontend expects the API at `http://127.0.0.1:8000`.

To use another API URL, set:

```text
NEXT_PUBLIC_API_URL=http://your-api-host:8000
```

## Risk score

The risk engine is deliberately simple and deterministic. The same input produces the same result, which makes the calculation easy to test and reason about.

The score combines four components:

| Component | Weight |
| --- | ---: |
| CVSS | 40% |
| Vulnerabilities | 25% |
| Asset risk | 20% |
| Security events | 15% |

The resulting score ranges from 0 to 100. A higher score means a better security posture.

The current levels are:

```text
80 to 100  low
60 to 79   medium
40 to 59   high
0 to 39    critical
```

The implementation lives in `backend/app/services/risk_engine.py`.

## Testing

Run the backend test suite with:

```bash
cd backend
source .venv/bin/activate
pytest -q
```

The test suite covers the risk calculation and the dashboard API. GitHub Actions runs the backend tests and frontend build on changes.

## Docker

Dockerfiles are included for the backend and frontend. The compose file is kept in the repository as the starting point for a container based setup. The current local development workflow uses the commands above.

## Security

Do not put API keys, passwords or other credentials into the repository.

Local SQLite databases and environment files are ignored by Git. If an NVD API key is used, provide it through an environment variable instead of committing it to source control.

The application is intended for development and portfolio use at this stage. Authentication, authorization, production database configuration and hardened deployment are still open work.

## Roadmap

The next useful additions would be:

- PostgreSQL support
- Authentication and role based access
- Asset detail pages
- Vulnerability remediation workflow
- More security event sources
- Historical risk scores
- Better CVE filtering and search
- Production deployment configuration
- More API and frontend tests

## License

No license has been selected yet. The repository is currently published as a portfolio project.
