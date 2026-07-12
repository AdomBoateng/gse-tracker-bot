from app.api.v1 import stocks, history, fx

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.models import snapshot_model  # noqa: F401 - registers DailySnapshot with Base

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Ghana Stock Exchange Information Platform API",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)
app.include_router(history.router)
app.include_router(fx.router)


@app.on_event("startup")
async def startup():
    """Create the snapshot database tables if they don't exist yet"""
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GSE Tracker API",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "gse_api": "connected"}
