# Security Dashboard

Ein Security Dashboard zur Überwachung von Assets, Schwachstellen und Sicherheitsereignissen.

Das Backend stellt eine REST API bereit und berechnet aus den vorhandenen Daten einen nachvollziehbaren Security Score. Das Frontend stellt diese Daten in einem übersichtlichen Dashboard dar.

Das Projekt ist als Portfolio Projekt gedacht. Die Struktur orientiert sich trotzdem an einer normalen Anwendung mit getrenntem Frontend, Backend, Datenbank, Tests und CI.

## Was das Projekt kann

Aktuell gibt es vier zentrale Bereiche:

1. Asset Verwaltung
2. Schwachstellenverwaltung
3. Erfassung von Sicherheitsereignissen
4. Risikobewertung

CVE Daten können über die NVD CVE API 2.0 abgerufen werden. Die importierten Daten werden vor dem Speichern normalisiert.

Das Dashboard ruft die Daten über die Backend API ab und zeigt Security Score, Risikostufe, Assets, Schwachstellen und die einzelnen Risikokomponenten an. Die Dashboard Daten werden alle 30 Sekunden aktualisiert.

## Technischer Aufbau

| Bereich | Technologie |
| --- | --- |
| Frontend | Next.js 15, React 19, TypeScript |
| Backend | FastAPI, Uvicorn |
| Datenbank | SQLite mit SQLAlchemy |
| Schwachstellendaten | NVD CVE API 2.0 |
| Tests | pytest, FastAPI TestClient |
| Container | Docker |
| CI | GitHub Actions |

## Projektstruktur

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

## Lokale Installation

### Backend

Für die Entwicklung wird Python 3.13 verwendet.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Die API ist danach unter folgendem Adresse erreichbar:

```text
http://127.0.0.1:8000
```

Wichtige Endpoints:

```text
GET  /health
GET  /api/v1
GET  /api/v1/assets
GET  /api/v1/vulnerabilities
GET  /api/v1/events
GET  /api/v1/dashboard/summary
POST /api/v1/vulnerabilities/import/{cve_id}
```

Beispiel für den Import einer CVE:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/vulnerabilities/import/CVE-2026-53647
```

### Frontend

In einem zweiten Terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Das Dashboard ist anschließend unter folgender Adresse erreichbar:

```text
http://localhost:3000
```

Standardmäßig erwartet das Frontend die API unter `http://127.0.0.1:8000`.

Wenn die API an einer anderen Adresse läuft, kann die URL über folgende Variable gesetzt werden:

```text
NEXT_PUBLIC_API_URL=http://dein-api-host:8000
```

## Security Score

Die Risikobewertung wird in `backend/app/services/risk_engine.py` berechnet.

Der Score liegt zwischen 0 und 100. Ein höherer Wert bedeutet eine bessere Sicherheitslage.

In die Berechnung fließen unter anderem ein:

- durchschnittlicher CVSS Wert
- Anzahl kritischer Schwachstellen
- Anzahl hoher Schwachstellen
- Risiko der vorhandenen Assets
- Anzahl der Sicherheitsereignisse

Die einzelnen Komponenten werden getrennt berechnet und anschließend gewichtet zusammengeführt.

## Tests

Die Backend Tests können mit folgendem Befehl ausgeführt werden:

```bash
cd backend
pytest -q
```

Die Tests prüfen unter anderem die Risk Engine und den Dashboard Endpoint über den FastAPI TestClient.

## Docker

Für die Container Umgebung stehen Dockerfiles für Backend und Frontend bereit.

```bash
docker compose up --build
```

## Sicherheit

Lokale Datenbanken, virtuelle Python Umgebungen und Umgebungsdateien werden nicht in Git eingecheckt.

NVD API Zugangsdaten dürfen nicht im Quellcode hinterlegt werden. Falls ein API Key verwendet wird, sollte dieser über eine Umgebungsvariable bereitgestellt werden.

## Entwicklungsstand

Das Projekt befindet sich in aktiver Entwicklung. Die aktuelle Version ist vor allem als Portfolio und technische Grundlage gedacht.

## Geplante Erweiterungen

- Authentifizierung und Benutzerverwaltung
- PostgreSQL Unterstützung
- Erweiterte Asset Verwaltung
- Verwaltung von Maßnahmen zur Behebung von Schwachstellen
- Import weiterer Security Events
- Historische Entwicklung des Security Scores
- Deployment für eine öffentliche Demo
