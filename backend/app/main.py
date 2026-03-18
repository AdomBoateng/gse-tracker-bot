from app.api.v1 import stocks

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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


@app.on_event("startup")
async def startup():
    """Initialize database on startup (if needed)"""
    pass


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
