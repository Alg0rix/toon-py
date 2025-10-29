"""
Pytest configuration and fixtures for TOON tests.

This module provides common fixtures and configuration for the test suite.
"""

import pytest
from toon_py import encode, decode


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "active": True,
        "skills": ["Python", "Mathematics", "Analytical Engine"],
        "profile": {
            "bio": "First computer programmer",
            "birth_year": 1815,
            "country": "United Kingdom"
        }
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return [
        {"sku": "BOOK-001", "name": "The Analytical Engine", "price": 29.99, "category": "Books"},
        {"sku": "COMP-002", "name": "Difference Engine", "price": 1999.99, "category": "Computers"},
        {"sku": "NOTE-003", "name": "Algorithm Notebook", "price": 12.50, "category": "Stationery"}
    ]


@pytest.fixture
def sample_analytics_data():
    """Sample analytics data for testing."""
    return {
        "metrics": [
            {"date": "2025-01-01", "page_views": 1250, "unique_visitors": 320, "bounce_rate": 0.35},
            {"date": "2025-01-02", "page_views": 1380, "unique_visitors": 345, "bounce_rate": 0.32},
            {"date": "2025-01-03", "page_views": 1190, "unique_visitors": 298, "bounce_rate": 0.38}
        ]
    }


@pytest.fixture
def special_characters_data():
    """Data with special characters for testing escaping."""
    return {
        "message": "Hello, world! This has: special characters",
        "path": "C:\\Users\\Admin\\Documents",
        "quote": 'She said: "TOON is great!"',
        "list": ["item with, comma", "item with: colon", "normal item"],
        "unicode": "Café naïve résumé 🌍",
        "emoji": ["🚀", "🎯", "💡", "📊"]
    }


def assert_roundtrip(data, **encode_options):
    """Assert that data round-trips correctly through encode/decode."""
    encoded = encode(data, **encode_options)
    decoded = decode(encoded)
    assert decoded == data, f"Roundtrip failed. Original: {data}, Decoded: {decoded}"
    return encoded, decoded


def assert_token_efficiency(data, min_savings_percent=0):
    """Assert that TOON provides token efficiency over JSON."""
    import json

    json_str = json.dumps(data, separators=(',', ':'))
    toon_str = encode(data)

    json_size = len(json_str)
    toon_size = len(toon_str)

    if json_size > 0:
        savings = ((json_size - toon_size) / json_size) * 100
        assert savings >= min_savings_percent, (
            f"TOON not efficient enough. JSON: {json_size}, "
            f"TOON: {toon_size}, Savings: {savings:.1f}% (min: {min_savings_percent}%)"
        )

    return json_size, toon_size, savings