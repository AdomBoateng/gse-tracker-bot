"""Test portfolio calculations"""

from app.services.portfolio_service import calculate_portfolio_stats
from app.models.portfolio_model import StockHolding
from datetime import datetime


def test_calculate_portfolio_stats():
    """Test portfolio statistics calculation"""
    holdings = [
        StockHolding(
            id=1,
            symbol="GLF",
            quantity=100,
            purchase_price=10.0,
            purchase_date="2024-01-01",
            current_price=12.0,
            current_value=1200.0,
            profit_loss=200.0,
            profit_loss_percent=20.0,
            created_at=datetime.now(),
        ),
        StockHolding(
            id=2,
            symbol="SIC",
            quantity=50,
            purchase_price=20.0,
            purchase_date="2024-01-01",
            current_price=18.0,
            current_value=900.0,
            profit_loss=-100.0,
            profit_loss_percent=-5.0,
            created_at=datetime.now(),
        ),
    ]

    stats = calculate_portfolio_stats(holdings)

    assert stats.stock_count == 2
    assert stats.total_value == 2100.0
    assert stats.total_cost == 2000.0
    assert stats.total_profit_loss == 100.0
    assert stats.total_profit_loss_percent == 5.0


def test_calculate_portfolio_stats_empty():
    """Test portfolio statistics with no holdings"""
    holdings = []

    stats = calculate_portfolio_stats(holdings)

    assert stats.stock_count == 0
    assert stats.total_value == 0.0
    assert stats.total_cost == 0.0
    assert stats.total_profit_loss == 0.0
