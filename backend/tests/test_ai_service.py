"""Test AI service"""

from app.services.ai_service import ai_service


def test_ai_service():
    """Test AI service initialization"""
    assert ai_service is not None
    assert ai_service.base_url is not None
