from fastapi import APIRouter, HTTPException
from typing import List
import json
import os

router = APIRouter(prefix="/api/v1/gse", tags=["gse"])

PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__) if __file__ else ""))
    )
)


def load_stocks_info() -> dict:
    """Load stock information from stocks.txt"""
    stocks_file = os.path.join(PROJECT_DIR, "stocks.txt")
    try:
        with open(stocks_file, "r") as f:
            data = json.load(f)
            return {stock["symbol"]: stock for stock in data.get("stocks", [])}
    except Exception:
        return {}


@router.get("/live", response_model=List[dict])
async def get_live_data():
    """Get live market data for all GSE stocks"""
    import httpx

    stocks_info = load_stocks_info()

    url = "https://dev.kwayisi.org/apis/gse/live"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            live_data = response.json()

            enriched_data = []
            for stock in live_data:
                symbol = stock.get("name")
                if symbol and symbol in stocks_info:
                    stock_info = stocks_info[symbol]
                    stock["company_name"] = stock_info.get(
                        "company_name", stock.get("name", "")
                    )
                    stock["logo_url"] = stock_info.get("logo_url")
                    stock["sector"] = stock_info.get("sector", "")
                else:
                    stock["symbol"] = symbol
                    stock["company_name"] = stock.get("name", "")
                    stock["logo_url"] = None
                    stock["sector"] = ""
                    stock["symbol"] = symbol or ""
                enriched_data.append(stock)

            return enriched_data
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching GSE data: {e}")


@router.get("/live/{symbol}", response_model=dict)
async def get_live_stock(symbol: str):
    """Get live data for a specific stock"""
    import httpx

    url = f"https://dev.kwayisi.org/apis/gse/live/{symbol}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")


@router.get("/equities", response_model=List[dict])
async def get_all_equities():
    """Get all equities summary"""
    import httpx

    url = "https://dev.kwayisi.org/apis/gse/equities"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching GSE data: {e}")


@router.get("/equities/{symbol}", response_model=dict)
async def get_equity(symbol: str):
    """Get detailed information for a specific stock"""
    import httpx

    url = f"https://dev.kwayisi.org/apis/gse/equities/{symbol}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
