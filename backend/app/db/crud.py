from app.db.session import Session
from typing import Optional
from app.models.portfolio_model import StockHolding
from app.services.gse_service import gse_service
from fastapi import HTTPException


def get_stock_holding(db: Session, stock_id: int) -> Optional[StockHolding]:
    """Get stock holding by ID"""
    return db.query(StockHolding).filter(StockHolding.id == stock_id).first()


def get_stock_by_symbol(db: Session, symbol: str) -> Optional[StockHolding]:
    """Get stock holding by symbol"""
    return db.query(StockHolding).filter(StockHolding.symbol == symbol).first()


def get_all_holdings(db: Session) -> list[StockHolding]:
    """Get all stock holdings"""
    return db.query(StockHolding).all()


async def create_stock_holding(
    db: Session, symbol: str, quantity: int, purchase_price: float, purchase_date: str
) -> StockHolding:
    """Create a new stock holding"""
    db_stock = StockHolding(
        symbol=symbol,
        quantity=quantity,
        purchase_price=purchase_price,
        purchase_date=purchase_date,
    )
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)

    live_data = await gse_service.get_live_stock(symbol)
    if live_data:
        current_price = live_data.price
        current_value = current_price * quantity
        cost = purchase_price * quantity
        profit_loss = current_value - cost
        profit_loss_percent = (profit_loss / cost * 100) if cost > 0 else 0.0

        db_stock.current_price = current_price
        db_stock.current_value = current_value
        db_stock.profit_loss = profit_loss
        db_stock.profit_loss_percent = profit_loss_percent

        db.commit()
        db.refresh(db_stock)

    return db_stock


def update_stock_holding(
    db: Session,
    stock_id: int,
    quantity: Optional[int] = None,
    purchase_price: Optional[float] = None,
    current_price: Optional[float] = None,
) -> Optional[StockHolding]:
    """Update stock holding"""
    db_stock = get_stock_holding(db, stock_id)
    if not db_stock:
        raise HTTPException(
            status_code=404, detail=f"Stock holding {stock_id} not found"
        )

    if quantity is not None:
        db_stock.quantity = quantity
    if purchase_price is not None:
        db_stock.purchase_price = purchase_price
    if (
        current_price is not None
        and db_stock.purchase_price is not None
        and db_stock.quantity is not None
    ):
        db_stock.current_price = current_price
        db_stock.current_value = current_price * db_stock.quantity
        cost = db_stock.purchase_price * db_stock.quantity
        db_stock.profit_loss = current_price * db_stock.quantity - cost
        if cost > 0:
            db_stock.profit_loss_percent = (db_stock.profit_loss / cost) * 100

    db.commit()
    db.refresh(db_stock)
    return db_stock


def delete_stock_holding(db: Session, stock_id: int) -> bool:
    """Delete stock holding"""
    db_stock = get_stock_holding(db, stock_id)
    if not db_stock:
        return False

    db.delete(db_stock)
    db.commit()
    return True
