"""Test GSE service"""

from app.services.gse_service import gse_service


def test_gse_service():
    """Test GSE service initialization"""
    assert gse_service is not None
    assert gse_service.base_url is not None
