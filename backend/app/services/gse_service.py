import asyncio
import json
import os
import time
from datetime import datetime, timezone
import httpx
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.db import crud
from app.db.session import SessionLocal
from app.models.stock import LiveStock, EquityInfo

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CACHE_TTL_SECONDS = 300
SHARES_CACHE_TTL_SECONDS = 24 * 60 * 60


class GSEService:
    """Service for interacting with GSE API"""

    def __init__(self):
        self.base_url = settings.gse_api_url
        self._stocks_info = self._load_stocks_info()
        self._live_cache: Optional[list[Dict[str, Any]]] = None
        self._live_cache_time: float = 0.0
        self._shares_cache: Optional[Dict[str, Optional[int]]] = None
        self._shares_cache_time: float = 0.0

    @staticmethod
    def _load_stocks_info() -> Dict[str, Dict[str, Any]]:
        """Load company metadata (name, logo, sector) from stocks.txt"""
        stocks_file = os.path.join(BACKEND_DIR, "stocks.txt")
        try:
            with open(stocks_file, "r") as f:
                data = json.load(f)
                return {stock["symbol"]: stock for stock in data.get("stocks", [])}
        except Exception:
            return {}

    def _stock_info_for(self, symbol: str) -> Dict[str, Any]:
        stock_info = self._stocks_info.get(symbol, {})
        if stock_info:
            return stock_info

        # stocks.txt may be updated while the dev server is running; reload once
        # when a live symbol is missing metadata instead of serving stale blanks.
        self._stocks_info = self._load_stocks_info()
        return self._stocks_info.get(symbol, {})

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

    async def get_live_data_enriched(self) -> list[Dict[str, Any]]:
        """Get live data enriched with company_name/logo_url/sector, cached for 5 minutes"""
        now = time.monotonic()
        if self._live_cache is not None and (now - self._live_cache_time) < CACHE_TTL_SECONDS:
            return self._live_cache

        data = await self._fetch_data("/live") or []

        enriched_data = []
        for stock in data:
            symbol = stock.get("name")
            stock_info = self._stock_info_for(symbol) if symbol else {}
            stock["symbol"] = symbol or ""
            stock["company_name"] = stock_info.get("company_name", stock.get("name", ""))
            stock["logo_url"] = stock_info.get("logo_url")
            stock["sector"] = stock_info.get("sector", "")
            enriched_data.append(stock)

        self._live_cache = enriched_data
        self._live_cache_time = now
        await self.maybe_capture_daily_snapshot()
        return enriched_data

    async def maybe_capture_daily_snapshot(self) -> None:
        """Capture one closing snapshot per stock for today, if not already done.

        Runs lazily on the first dashboard request after market close each day,
        rather than on a fixed schedule - this needs no cron/APScheduler and
        works fine on free-tier hosts that spin down when idle.
        """
        now = datetime.now(timezone.utc)
        if now.weekday() >= 5:  # Saturday=5, Sunday=6 - market never opens
            return
        if now.hour < 15:  # GSE closes 15:00 UTC
            return

        date_str = now.strftime("%Y-%m-%d")
        db = SessionLocal()
        try:
            if crud.snapshot_exists_for_date(db, date_str):
                return
            rows = await self._build_market_rows()
            crud.bulk_insert_snapshots(db, date_str, rows)
        finally:
            db.close()

    def refresh_cache(self):
        """Manually invalidate the cached live data"""
        self._live_cache = None

    async def get_shares_outstanding_cached(self) -> Dict[str, Optional[int]]:
        """Get shares outstanding per symbol, cached for 24h.

        The bulk /equities endpoint returns null shares/capital for every stock -
        only the per-symbol /equities/{symbol} detail endpoint has real values,
        so this fetches all symbols concurrently and caches the result.
        """
        now = time.monotonic()
        if (
            self._shares_cache is not None
            and (now - self._shares_cache_time) < SHARES_CACHE_TTL_SECONDS
        ):
            return self._shares_cache

        # The upstream API rate-limits (429s) on concurrent bursts, so fetch sequentially
        # with a small delay - this only runs once per 24h, so the extra time is fine.
        symbols = list(self._stocks_info.keys())
        shares_by_symbol: Dict[str, Optional[int]] = {}
        for symbol in symbols:
            result = await self._fetch_data(f"/equities/{symbol}")
            shares_by_symbol[symbol] = result["shares"] if isinstance(result, dict) and result.get("shares") else None
            await asyncio.sleep(0.25)

        self._shares_cache = shares_by_symbol
        self._shares_cache_time = now
        return shares_by_symbol

    async def _build_market_rows(self) -> List[Dict[str, Any]]:
        """Combine live prices with cached shares outstanding into per-stock market cap rows"""
        live_data = await self.get_live_data_enriched()
        shares_by_symbol = await self.get_shares_outstanding_cached()

        rows = []
        for stock in live_data:
            symbol = stock.get("symbol")
            shares = shares_by_symbol.get(symbol)
            price = stock.get("price", 0.0)
            change = stock.get("change", 0.0)
            volume = stock.get("volume", 0) or 0
            market_cap = shares * price if shares else None
            rows.append(
                {
                    "symbol": symbol,
                    "price": price,
                    "change": change,
                    "volume": volume,
                    "market_cap": market_cap,
                }
            )
        return rows

    async def get_market_composite(self) -> Dict[str, Any]:
        """Market-cap-weighted composite % change across all stocks with known shares.

        This is an unofficial proxy for overall market performance, not the real
        GSE Composite Index (which requires GSE's non-public base-period figures).
        """
        rows = await self._build_market_rows()

        total_market_cap = 0.0
        weighted_change_sum = 0.0
        total_volume = 0

        for row in rows:
            total_volume += row["volume"]
            market_cap = row["market_cap"]
            price = row["price"]
            change = row["change"]
            if not market_cap or not price:
                continue

            prev_price = price - change
            percent_change = (change / prev_price * 100) if prev_price else 0.0
            total_market_cap += market_cap
            weighted_change_sum += market_cap * percent_change

        composite_change_percent = (
            weighted_change_sum / total_market_cap if total_market_cap > 0 else 0.0
        )

        return {
            "composite_change_percent": round(composite_change_percent, 4),
            "total_market_cap": total_market_cap,
            "total_volume": total_volume,
            "stock_count": len(rows),
        }


gse_service = GSEService()
