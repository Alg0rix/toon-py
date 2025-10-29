"""
Tabular array tests for TOON Python implementation.

Tests the tabular format optimization for uniform arrays of objects.
"""

import pytest
from toon_py import encode, decode


class TestTabularArrays:
    """Test encoding/decoding of tabular arrays."""

    def test_simple_tabular(self):
        """Test simple tabular array."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        result = encode(data)
        expected = "users[2]{id,name}:\n  1,Alice\n  2,Bob"
        assert result == expected
        decoded = decode(result)
        assert decoded == data

    def test_three_fields_tabular(self):
        """Test tabular array with three fields."""
        data = {
            "products": [
                {"sku": "A1", "name": "Widget", "price": 9.99},
                {"sku": "B2", "name": "Gadget", "price": 14.50}
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "products[2]{sku,name,price}:"
        assert "  A1,Widget,9.99" in lines
        assert "  B2,Gadget,14.5" in lines
        decoded = decode(result)
        assert decoded == data

    def test_single_row_tabular(self):
        """Test tabular array with single row."""
        data = {
            "config": [
                {"key": "timeout", "value": 30, "enabled": True}
            ]
        }
        result = encode(data)
        assert result == "config[1]{key,value,enabled}:\n  timeout,30,true"
        decoded = decode(result)
        assert decoded == data

    def test_many_rows_tabular(self):
        """Test tabular array with many rows."""
        data = {
            "metrics": [
                {"date": "2025-01-01", "value": 100},
                {"date": "2025-01-02", "value": 150},
                {"date": "2025-01-03", "value": 120},
                {"date": "2025-01-04", "value": 180},
                {"date": "2025-01-05", "value": 200}
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "metrics[5]{date,value}:"
        assert len(lines) == 6  # header + 5 rows
        decoded = decode(result)
        assert decoded == data

    def test_tabular_with_special_values(self):
        """Test tabular array with values requiring escaping."""
        data = {
            "messages": [
                {"text": "Hello, world!", "sender": "Alice"},
                {"text": "Good morning", "sender": "Bob"}
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "messages[2]{text,sender}:"
        assert '  "Hello, world!",Alice' in lines
        assert "  Good morning,Bob" in lines
        decoded = decode(result)
        assert decoded == data

    def test_tabular_numeric_types(self):
        """Test tabular array with different numeric types."""
        data = {
            "data": [
                {"int": 42, "float": 3.14, "neg": -17},
                {"int": 100, "float": -2.5, "neg": 0}
            ]
        }
        result = encode(data)
        expected = "data[2]{int,float,neg}:\n  42,3.14,-17\n  100,-2.5,0"
        assert result == expected
        decoded = decode(result)
        assert decoded == data

    def test_tabular_booleans_and_nulls(self):
        """Test tabular array with booleans and nulls."""
        data = {
            "records": [
                {"active": True, "verified": False, "notes": None},
                {"active": False, "verified": True, "notes": "test"}
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "records[2]{active,verified,notes}:"
        assert "  true,false,null" in lines
        assert "  false,true,test" in lines
        decoded = decode(result)
        assert decoded == data


class TestNonTabularFallback:
    """Test cases where tabular format should not be used."""

    def test_mixed_object_types(self):
        """Test array with mixed object types - should use list format."""
        data = {
            "items": [
                {"id": 1, "name": "Alice"},
                "string",  # Not an object
                {"id": 2, "name": "Bob"}
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "items[3]:"
        assert "- string" in result
        assert "- id: 1" in result
        assert "- id: 2" in result
        decoded = decode(result)
        assert decoded == data

    def test_different_keys(self):
        """Test array with objects having different keys - should use list format."""
        data = {
            "items": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "title": "Manager"}  # Different key name
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "items[2]:"
        assert "- id: 1" in result
        assert "  name: Alice" in result
        assert "- id: 2" in result
        assert "  title: Manager" in result
        decoded = decode(result)
        assert decoded == data

    def test_missing_keys(self):
        """Test array with objects missing keys - should use list format."""
        data = {
            "items": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob"}  # Missing 'role' key
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "items[2]:"
        assert "- id: 1" in result
        assert "  role: admin" in result
        assert "- id: 2" in result
        decoded = decode(result)
        assert decoded == data

    def test_nested_values(self):
        """Test array with objects containing nested values - should use list format."""
        data = {
            "items": [
                {"id": 1, "profile": {"name": "Alice"}},  # Nested object
                {"id": 2, "tags": ["a", "b"]}  # Nested array
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "items[2]:"
        assert "- id: 1" in result
        assert "  profile:" in result
        assert "- id: 2" in result
        decoded = decode(result)
        assert decoded == data

    def test_empty_objects(self):
        """Test array with empty objects - should use list format."""
        data = {
            "items": [
                {"id": 1, "name": "Alice"},
                {}  # Empty object
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "items[2]:"
        assert "- id: 1" in result
        assert "- " in result  # Empty object
        decoded = decode(result)
        assert decoded == data


class TestTabularWithDifferentDelimiters:
    """Test tabular arrays with different delimiters."""

    def test_tab_delimiter(self):
        """Test tabular array with tab delimiter."""
        data = {
            "items": [
                {"name": "Item A", "desc": "Description with, commas"},
                {"name": "Item B", "desc": "Another, description"}
            ]
        }
        result = encode(data, delimiter='tab')
        lines = result.split('\n')
        assert lines[0] == "items[2\t]{name\tdesc}:"
        assert "Item A\tDescription with, commas" in lines[1]
        assert "Item B\tAnother, description" in lines[2]
        decoded = decode(result)
        assert decoded == data

    def test_pipe_delimiter(self):
        """Test tabular array with pipe delimiter."""
        data = {
            "data": [
                {"field1": "value1", "field2": "value2"},
                {"field1": "value3", "field2": "value4"}
            ]
        }
        result = encode(data, delimiter='pipe')
        lines = result.split('\n')
        assert lines[0] == "data[2|]{field1|field2}:"
        assert "value1|value2" in lines[1]
        assert "value3|value4" in lines[2]
        decoded = decode(result)
        assert decoded == data


class TestRootTabularArrays:
    """Test root-level tabular arrays."""

    def test_root_tabular_array(self):
        """Test root-level tabular array."""
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        result = encode(data)
        expected = "[2]{id,name}:\n  1,Alice\n  2,Bob"
        assert result == expected
        decoded = decode(result)
        assert decoded == data

    def test_root_single_row_tabular(self):
        """Test root-level tabular array with single row."""
        data = [{"key": "test", "value": 42}]
        result = encode(data)
        assert result == "[1]{key,value}:\n  test,42"
        decoded = decode(result)
        assert decoded == data


if __name__ == "__main__":
    pytest.main([__file__])