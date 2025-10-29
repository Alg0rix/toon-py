"""
Basic encoding tests for TOON Python implementation.

Tests core functionality including primitives, objects, and arrays.
"""

import pytest
from toon_py import encode, decode


class TestPrimitives:
    """Test encoding/decoding of primitive values."""

    @pytest.mark.parametrize("value,expected_toon", [
        (None, "null"),
        (True, "true"),
        (False, "false"),
        (0, "0"),
        (42, "42"),
        (-17, "-17"),
        (3.14, "3.14"),
        (-0.5, "-0.5"),
        ("hello", "hello"),
        ("", '""'),
        ("hello world", "hello world"),
        ("hello, world", '"hello, world"'),
        ("a:b", '"a:b"'),
        ("true", '"true"'),
        ("false", '"false"'),
        ("null", '"null"'),
        ("42", '"42"'),
        ("-3.14", '"-3.14"'),
        (" leading", '" leading"'),
        ("trailing ", '"trailing "'),
        ("- item", '"- item"'),
        ("[1,2,3]", '"[1,2,3]"'),
        ("{key:value}", '"{key:value}"'),
    ])
    def test_primitive_encoding(self, value, expected_toon):
        """Test encoding of primitive values."""
        result = encode(value)
        assert result == expected_toon

    @pytest.mark.parametrize("value", [
        None, True, False, 0, 42, -17, 3.14, -0.5,
        "hello", "", "hello world", "hello, world"
    ])
    def test_primitive_roundtrip(self, value):
        """Test that primitive values round-trip correctly."""
        encoded = encode(value)
        decoded = decode(encoded)
        assert decoded == value


class TestSimpleObjects:
    """Test encoding/decoding of simple objects."""

    def test_empty_object(self):
        """Test empty object."""
        data = {}
        result = encode(data)
        assert result == ""
        decoded = decode(result)
        assert decoded == {}

    def test_single_field_object(self):
        """Test object with single field."""
        data = {"name": "Ada"}
        result = encode(data)
        assert result == "name: Ada"
        decoded = decode(result)
        assert decoded == data

    def test_multiple_field_object(self):
        """Test object with multiple fields."""
        data = {"name": "Ada", "age": 30, "active": True}
        result = encode(data)
        lines = result.split('\n')
        assert "name: Ada" in lines
        assert "age: 30" in lines
        assert "active: true" in lines
        decoded = decode(result)
        assert decoded == data

    def test_object_escaping(self):
        """Test object key and value escaping."""
        data = {
            "user name": "Ada Lovelace",
            "special:key": "value:with:colons",
            "quoted": "contains, commas",
            "normal_key": "normal value"
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data


class TestNestedObjects:
    """Test encoding/decoding of nested objects."""

    def test_simple_nested(self):
        """Test simple nested object."""
        data = {
            "user": {
                "name": "Ada",
                "age": 30
            }
        }
        result = encode(data)
        lines = result.split('\n')
        assert "user:" in lines
        assert "  name: Ada" in lines
        assert "  age: 30" in lines
        decoded = decode(result)
        assert decoded == data

    def test_deeply_nested(self):
        """Test deeply nested objects."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "value": "deep"
                    }
                }
            }
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data

    def test_nested_with_arrays(self):
        """Test nested objects containing arrays."""
        data = {
            "user": {
                "name": "Ada",
                "tags": ["python", "ai"],
                "profile": {
                    "bio": "Developer",
                    "active": True
                }
            }
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data


class TestPrimitiveArrays:
    """Test encoding/decoding of primitive arrays."""

    def test_empty_array(self):
        """Test empty array."""
        data = {"items": []}
        result = encode(data)
        assert result == "items[0]:"
        decoded = decode(result)
        assert decoded == data

    def test_single_element_array(self):
        """Test single element array."""
        data = {"items": ["hello"]}
        result = encode(data)
        assert result == "items[1]: hello"
        decoded = decode(result)
        assert decoded == data

    def test_string_array(self):
        """Test array of strings."""
        data = {"tags": ["python", "ai", "developer"]}
        result = encode(data)
        assert result == "tags[3]: python,ai,developer"
        decoded = decode(result)
        assert decoded == data

    def test_number_array(self):
        """Test array of numbers."""
        data = {"numbers": [1, 2, 3.5, -4]}
        result = encode(data)
        assert result == "numbers[4]: 1,2,3.5,-4"
        decoded = decode(result)
        assert decoded == data

    def test_mixed_primitive_array(self):
        """Test array of mixed primitives."""
        data = {"mixed": [True, False, None]}
        result = encode(data)
        assert result == "mixed[3]: true,false,null"
        decoded = decode(result)
        assert decoded == data

    def test_array_escaping(self):
        """Test array values requiring escaping."""
        data = {"items": ["hello, world", "a:b", "normal"]}
        result = encode(data)
        assert result == 'items[3]: "hello, world","a:b",normal'
        decoded = decode(result)
        assert decoded == data


class TestRootArray:
    """Test encoding/decoding of root arrays."""

    def test_root_primitive_array(self):
        """Test root array of primitives."""
        data = ["a", "b", "c"]
        result = encode(data)
        assert result == "[3]: a,b,c"
        decoded = decode(result)
        assert decoded == data

    def test_root_number_array(self):
        """Test root array of numbers."""
        data = [1, 2, 3]
        result = encode(data)
        assert result == "[3]: 1,2,3"
        decoded = decode(result)
        assert decoded == data

    def test_root_empty_array(self):
        """Test empty root array."""
        data = []
        result = encode(data)
        assert result == "[0]:"
        decoded = decode(result)
        assert decoded == data


if __name__ == "__main__":
    pytest.main([__file__])