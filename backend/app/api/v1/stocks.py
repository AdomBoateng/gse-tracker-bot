from fastapi import APIRouter, HTTPException
from typing import List

from app.models.stock import EquityInfo, LiveStock
from app.services.gse_service import gse_service

router = APIRouter(prefix="/api/v1/gse", tags=["gse"])


@router.get("/live", response_model=List[dict])
async def get_live_data():
    """Get live market data for all GSE stocks, enriched with company info"""
    return await gse_service.get_live_data_enriched()


@router.get("/live/{symbol}", response_model=LiveStock)
async def get_live_stock(symbol: str):
    """Get live data for a specific stock"""
    stock = await gse_service.get_live_stock(symbol)
    if stock is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return stock


@router.get("/equities", response_model=List[EquityInfo])
async def get_all_equities():
    """Get all equities summary"""
    return await gse_service.get_equities()


@router.get("/equities/{symbol}", response_model=EquityInfo)
async def get_equity(symbol: str):
    """Get detailed information for a specific stock"""
    equity = await gse_service.get_equity_info(symbol)
    if equity is None:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return equity
