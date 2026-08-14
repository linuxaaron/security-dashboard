from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.security import router as security_router
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Security Dashboard API",
    description=(
        "REST API for security monitoring, vulnerabilities, "
        "assets and events."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(
    security_router,
    prefix="/api/v1",
    tags=["security"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1", tags=["system"])
async def api_info() -> dict[str, str]:
    return {
        "name": "Security Dashboard API",
        "version": "0.2.0",
        "status": "development",
    }
