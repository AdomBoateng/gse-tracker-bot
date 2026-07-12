from fastapi import APIRouter, HTTPException

from app.services.fx_service import fx_service

router = APIRouter(prefix="/api/v1/fx", tags=["fx"])


@router.get("/rates")
async def get_rates(base: str = "GHS", symbols: str = "USD,GBP,EUR"):
    """Currency conversion rates, e.g. GHS -> USD/GBP/EUR"""
    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    data = await fx_service.get_rates(base=base, symbols=symbol_list)
    if data is None:
        raise HTTPException(status_code=502, detail="Unable to fetch FX rates")
    return data
