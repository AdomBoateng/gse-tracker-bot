import csv
import io
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db import crud
from app.db.session import get_db
from app.services.gse_service import gse_service

router = APIRouter(prefix="/api/v1/gse", tags=["gse-history"])


@router.get("/composite")
async def get_composite():
    """Today's market-cap-weighted composite % change (unofficial proxy, not the real GSE-CI)"""
    return await gse_service.get_market_composite()


@router.get("/history/composite")
async def get_composite_history(days: int = 30, db: Session = Depends(get_db)):
    """Daily composite % change history, derived from stored snapshots"""
    rows = crud.get_snapshots_in_range(db, days)

    by_date = defaultdict(list)
    for row in rows:
        by_date[row.date].append(row)

    result = []
    for date_str in sorted(by_date.keys()):
        total_market_cap = 0.0
        weighted_sum = 0.0
        for row in by_date[date_str]:
            if not row.market_cap or not row.price:
                continue
            prev_price = row.price - row.change
            percent_change = (row.change / prev_price * 100) if prev_price else 0.0
            total_market_cap += row.market_cap
            weighted_sum += row.market_cap * percent_change

        composite = weighted_sum / total_market_cap if total_market_cap > 0 else 0.0
        result.append({"date": date_str, "composite_change_percent": round(composite, 4)})

    return result


@router.get("/history/{symbol}")
async def get_symbol_history(symbol: str, days: int = 30, db: Session = Depends(get_db)):
    """Daily price history for a single stock, from stored snapshots"""
    rows = crud.get_symbol_history(db, symbol, days)
    return [
        {"date": r.date, "price": r.price, "change": r.change, "volume": r.volume}
        for r in rows
    ]


@router.get("/export/csv")
async def export_csv():
    """Download today's live market data as CSV"""
    data = await gse_service.get_live_data_enriched()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Symbol", "Company", "Sector", "Price (GHS)", "Change", "% Change", "Volume"])

    for stock in data:
        price = stock.get("price", 0.0)
        change = stock.get("change", 0.0)
        prev_price = price - change
        percent_change = (change / prev_price * 100) if prev_price else 0.0
        writer.writerow(
            [
                stock.get("symbol", ""),
                stock.get("company_name", ""),
                stock.get("sector", ""),
                f"{price:.2f}",
                f"{change:.2f}",
                f"{percent_change:.2f}",
                stock.get("volume", 0),
            ]
        )

    filename = f"gse_live_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
