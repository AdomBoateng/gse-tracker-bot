"""Test CSV export endpoint"""

from fastapi.testclient import TestClient

from app.main import app
from app.services.gse_service import gse_service

client = TestClient(app)


def test_export_csv(monkeypatch):
    async def fake_enriched():
        return [
            {
                "symbol": "TEST",
                "company_name": "Test Co",
                "sector": "Testing",
                "price": 10.0,
                "change": 1.0,
                "volume": 100,
            }
        ]

    monkeypatch.setattr(gse_service, "get_live_data_enriched", fake_enriched)

    response = client.get("/api/v1/gse/export/csv")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment" in response.headers["content-disposition"]
    assert "TEST" in response.text
    assert "Test Co" in response.text
