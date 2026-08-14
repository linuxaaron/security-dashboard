from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Security Dashboard API",
    description="REST API for security monitoring, vulnerabilities, assets and events.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Return the API health status."""
    return {"status": "ok"}


@app.get("/api/v1", tags=["system"])
async def api_info() -> dict[str, str]:
    """Return basic API information."""
    return {
        "name": "Security Dashboard API",
        "version": "0.1.0",
        "status": "development",
    }
