"""Test market-cap-weighted composite calculation"""

import pytest

from app.services.gse_service import GSEService


@pytest.mark.asyncio
async def test_get_market_composite_weighting():
    service = GSEService.__new__(GSEService)  # skip __init__ (no stocks.txt/network needed)

    async def fake_build_rows():
        return [
            {"symbol": "A", "price": 10.0, "change": 1.0, "volume": 100, "market_cap": 1000.0},
            {"symbol": "B", "price": 20.0, "change": -2.0, "volume": 200, "market_cap": 3000.0},
            {"symbol": "C", "price": 5.0, "change": 0.0, "volume": 50, "market_cap": None},
        ]

    service._build_market_rows = fake_build_rows

    result = await service.get_market_composite()

    # A: prev=9.0, pct=+11.111...%, weight 1000
    # B: prev=22.0, pct=-9.0909...%, weight 3000
    # C: excluded - no market_cap
    expected = (1000 * (1 / 9 * 100) + 3000 * (-2 / 22 * 100)) / (1000 + 3000)

    assert result["composite_change_percent"] == pytest.approx(round(expected, 4), abs=0.001)
    assert result["total_market_cap"] == 4000.0
    assert result["total_volume"] == 350
    assert result["stock_count"] == 3


@pytest.mark.asyncio
async def test_get_market_composite_no_market_cap_data():
    service = GSEService.__new__(GSEService)

    async def fake_build_rows():
        return [
            {"symbol": "A", "price": 10.0, "change": 1.0, "volume": 100, "market_cap": None},
        ]

    service._build_market_rows = fake_build_rows

    result = await service.get_market_composite()

    assert result["composite_change_percent"] == 0.0
    assert result["total_market_cap"] == 0.0
