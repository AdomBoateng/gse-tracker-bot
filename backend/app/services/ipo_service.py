import json
import os
from typing import Any, Dict, List, Optional

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)


class IPOService:
    """Serves a curated dataset of GSE company listings (IPOs) with pros and cons.

    The content is static, editorial reference data kept in app/data/ipos.json -
    it does not change intraday, so it is loaded once and held in memory.
    """

    def __init__(self):
        self._stocks_info = self._load_stocks_info()
        self._data = self._load()

    @staticmethod
    def _load() -> Dict[str, Any]:
        path = os.path.join(DATA_DIR, "ipos.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"disclaimer": "", "ipos": []}

    @staticmethod
    def _load_stocks_info() -> Dict[str, Dict[str, Any]]:
        path = os.path.join(BACKEND_DIR, "stocks.txt")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {stock["symbol"]: stock for stock in data.get("stocks", [])}
        except Exception:
            return {}

    def _enrich_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        symbol = str(entry.get("symbol", "")).upper()
        stock_info = self._stocks_info.get(symbol, {})
        return {
            **entry,
            "logo_url": stock_info.get("logo_url"),
            "sector": entry.get("sector") or stock_info.get("sector", ""),
        }

    def get_all(self) -> Dict[str, Any]:
        """Return the full IPO list plus the shared disclaimer."""
        return {
            "disclaimer": self._data.get("disclaimer", ""),
            "ipos": [self._enrich_entry(entry) for entry in self._data.get("ipos", [])],
        }

    def get_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return a single company's IPO entry (case-insensitive), or None."""
        target = symbol.upper()
        for entry in self._data.get("ipos", []):
            if str(entry.get("symbol", "")).upper() == target:
                return self._enrich_entry(entry)
        return None

    def symbols(self) -> List[str]:
        """Symbols that have a curated IPO entry."""
        return [entry.get("symbol", "") for entry in self._data.get("ipos", [])]


ipo_service = IPOService()
