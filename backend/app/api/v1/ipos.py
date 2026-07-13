from fastapi import APIRouter, HTTPException

from app.services.ipo_service import ipo_service

router = APIRouter(prefix="/api/v1/ipos", tags=["ipos"])


@router.get("")
async def get_ipos():
    """Curated list of GSE company listings (IPOs) with pros and cons."""
    return ipo_service.get_all()


@router.get("/{symbol}")
async def get_ipo(symbol: str):
    """Curated IPO pros/cons for a single company by symbol."""
    entry = ipo_service.get_by_symbol(symbol)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"No IPO entry for {symbol}")
    return entry
