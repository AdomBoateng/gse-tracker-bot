import time
from typing import Any, Dict, List, Optional

import httpx

# Frankfurter (ECB-based) does not carry GHS - confirmed by direct testing, not just
# docs, since GHS is absent from its /currencies list and both base=GHS and
# symbols=GHS 404. open.er-api.com (exchangerate-api.com's free, keyless endpoint)
# does carry GHS, so that's used here instead.
ER_API_URL = "https://open.er-api.com/v6/latest"
CACHE_TTL_SECONDS = 60 * 60  # rates only update once a day upstream


class FXService:
    """Currency conversion rates, proxied from the free/keyless exchangerate-api.com endpoint"""

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_time: Dict[str, float] = {}

    async def get_rates(
        self, base: str = "GHS", symbols: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        symbols = symbols or ["USD", "GBP", "EUR"]
        cache_key = base
        now = time.monotonic()
        if cache_key in self._cache and (now - self._cache_time[cache_key]) < CACHE_TTL_SECONDS:
            data = self._cache[cache_key]
        else:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{ER_API_URL}/{base}", timeout=15.0)
                    response.raise_for_status()
                    data = response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching FX rates: {e}")
                data = self._cache.get(cache_key)
                if data is None:
                    return None

            self._cache[cache_key] = data
            self._cache_time[cache_key] = now

        all_rates = data.get("rates", {})
        return {
            "base": data.get("base_code", base),
            "date": data.get("time_last_update_utc"),
            "rates": {symbol: all_rates[symbol] for symbol in symbols if symbol in all_rates},
        }


fx_service = FXService()
