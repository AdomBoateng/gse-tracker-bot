import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
from app.models.stock import LiveStock, EquityInfo
from cachetools import TTLCache, cached

# Cache with 5-minute TTL
stock_cache = TTLCache(maxsize=100, ttl=300)


class GSEService:
    """Service for interacting with GSE API"""

    def __init__(self):
        self.base_url = settings.gse_api_url

    async def _fetch_data(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Make async HTTP request to GSE API"""
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            print(f"Error fetching data from {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    async def get_live_data(self) -> list[LiveStock]:
        """Get live trading data for all GSE stocks"""
        data = await self._fetch_data("/live")
        if data:
            return [LiveStock.model_validate(stock) for stock in data]
        return []

    async def get_live_stock(self, symbol: str) -> LiveStock | None:
        """Get live data for a specific stock"""
        data = await self._fetch_data(f"/live/{symbol}")
        if data:
            return LiveStock.model_validate(data)
        return None

    async def get_equities(self) -> list[EquityInfo]:
        """Get summary of all equities"""
        data = await self._fetch_data("/equities")
        if data:
            return [EquityInfo.model_validate(eq) for eq in data]
        return []

    async def get_equity_info(self, symbol: str) -> EquityInfo | None:
        """Get detailed information for a specific stock"""
        data = await self._fetch_data(f"/equities/{symbol}")
        if data:
            return EquityInfo.model_validate(data)
        return None

    @cached(stock_cache)
    def get_live_data_cached(self) -> list[Dict[str, Any]]:
        """Get cached live data (blocking version)"""
        import httpx

        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/live", timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error fetching cached data: {e}")
            return []

    def refresh_cache(self):
        """Manually refresh cache"""
        stock_cache.clear()


gse_service = GSEService()
