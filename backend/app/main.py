"""
FastAPI application factory.
Configures CORS, registers all routers under /api/v1, and runs DB init on startup.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import (
    meetings_router,
    transcripts_router,
    summaries_router,
    action_items_router,
    search_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup tasks (DB init) before serving requests."""
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fireflies Clone API",
        description="Meeting notes & transcription platform API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — allow Next.js dev server
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register all routers under /api/v1
    prefix = "/api/v1"
    app.include_router(meetings_router, prefix=prefix)
    app.include_router(transcripts_router, prefix=prefix)
    app.include_router(summaries_router, prefix=prefix)
    app.include_router(action_items_router, prefix=prefix)
    app.include_router(search_router, prefix=prefix)

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "service": "fireflies-clone-api"}

    return app


app = create_app()
