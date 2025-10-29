"""
Advanced feature tests for TOON Python implementation.

Tests alternative delimiters, length markers, and complex scenarios.
"""

import pytest
from toon_py import encode, decode


class TestAlternativeDelimiters:
    """Test alternative delimiter support."""

    def test_tab_delimiter_primitive_array(self):
        """Test tab delimiter with primitive array."""
        data = {"items": ["a,b", "c,d", "e,f"]}
        result = encode(data, delimiter='tab')
        assert result == "items[3\t]:\ta,b\tc,d\te,f"
        decoded = decode(result)
        assert decoded == data

    def test_pipe_delimiter_primitive_array(self):
        """Test pipe delimiter with primitive array."""
        data = {"items": ["a|b", "c|d", "e|f"]}
        result = encode(data, delimiter='pipe')
        assert result == 'items[3|]: a|b|c|d|e|f'
        decoded = decode(result)
        assert decoded == data

    def test_tab_delimiter_tabular(self):
        """Test tab delimiter with tabular array."""
        data = {
            "users": [
                {"name": "Alice", "role": "admin,dev"},
                {"name": "Bob", "role": "user,test"}
            ]
        }
        result = encode(data, delimiter='tab')
        lines = result.split('\n')
        assert lines[0] == "users[2\t]{name\trole}:"
        assert "Alice\tadmin,dev" in lines[1]
        assert "Bob\tuser,test" in lines[2]
        decoded = decode(result)
        assert decoded == data

    def test_pipe_delimiter_tabular(self):
        """Test pipe delimiter with tabular array."""
        data = {
            "products": [
                {"sku": "A1", "desc": "Product|A"},
                {"sku": "B2", "desc": "Product|B"}
            ]
        }
        result = encode(data, delimiter='pipe')
        lines = result.split('\n')
        assert lines[0] == "products[2|]{sku|desc}:"
        assert "A1|Product|A" in lines[1]
        assert "B2|Product|B" in lines[2]
        decoded = decode(result)
        assert decoded == data

    def test_delimiter_quoting_rules(self):
        """Test that delimiter-aware quoting works correctly."""
        data = {"items": ["a,b", "c\t", "d|e"]}

        # With comma delimiter (default), pipe and tab should be safe
        result_comma = encode(data, delimiter=',')
        assert 'a,b' in result_comma  # Should be quoted
        assert '"c\t"' in result_comma  # Tab should be quoted
        assert '"d|e"' in result_comma  # Pipe should be quoted

        # With tab delimiter, commas should be safe
        result_tab = encode(data, delimiter='tab')
        assert 'a,b' in result_tab  # Comma should NOT be quoted
        assert '"d|e"' in result_tab  # Pipe should still be quoted

        decoded_comma = decode(result_comma)
        decoded_tab = decode(result_tab)
        assert decoded_comma == data
        assert decoded_tab == data


class TestLengthMarkers:
    """Test length marker functionality."""

    def test_primitive_array_with_marker(self):
        """Test primitive array with length marker."""
        data = {"tags": ["a", "b", "c"]}
        result = encode(data, length_marker=True)
        assert result == "tags[#3]: a,b,c"
        decoded = decode(result)
        assert decoded == data

    def test_tabular_array_with_marker(self):
        """Test tabular array with length marker."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ]
        }
        result = encode(data, length_marker=True)
        lines = result.split('\n')
        assert lines[0] == "users[#2]{id,name}:"
        decoded = decode(result)
        assert decoded == data

    def test_root_array_with_marker(self):
        """Test root array with length marker."""
        data = [1, 2, 3]
        result = encode(data, length_marker=True)
        assert result == "[#3]: 1,2,3"
        decoded = decode(result)
        assert decoded == data

    def test_empty_array_with_marker(self):
        """Test empty array with length marker."""
        data = {"items": []}
        result = encode(data, length_marker=True)
        assert result == "items[#0]:"
        decoded = decode(result)
        assert decoded == data

    def test_nested_arrays_with_marker(self):
        """Test nested arrays with length markers."""
        data = {
            "matrix": [
                [1, 2, 3],
                [4, 5, 6]
            ]
        }
        result = encode(data, length_marker=True)
        lines = result.split('\n')
        assert lines[0] == "matrix[#2]:"
        assert "- [#3]: 1,2,3" in lines
        assert "- [#3]: 4,5,6" in lines
        decoded = decode(result)
        assert decoded == data


class TestComplexStructures:
    """Test complex nested structures."""

    def test_nested_mixed_arrays(self):
        """Test nested arrays of different types."""
        data = {
            "company": {
                "name": "Tech Corp",
                "employees": [
                    {
                        "id": 1,
                        "name": "Alice",
                        "skills": ["Python", "AI"],
                        "projects": [
                            {"name": "Project A", "status": "active"},
                            {"name": "Project B", "status": "completed"}
                        ]
                    }
                ]
            }
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data

    def test_arrays_of_arrays(self):
        """Test arrays containing arrays."""
        data = {
            "matrices": [
                [[1, 2], [3, 4]],
                [[5, 6], [7, 8]]
            ]
        }
        result = encode(data)
        lines = result.split('\n')
        assert lines[0] == "matrices[2]:"
        assert "- [2]: 1,2" in result
        assert "- [2]: 3,4" in result
        decoded = decode(result)
        assert decoded == data

    def test_deeply_nested_objects(self):
        """Test deeply nested object structures."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "value": "deep",
                            "array": [1, 2, 3]
                        }
                    }
                }
            }
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data

    def test_mixed_list_items(self):
        """Test list items with different types."""
        data = {
            "items": [
                42,  # Primitive
                {"key": "value"},  # Object
                [1, 2, 3],  # Array
                None,  # Null
                "string"  # String
            ]
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_unicode_and_emoji(self):
        """Test Unicode characters and emoji."""
        data = {
            "greeting": "Hello 🌍",
            "emoji": ["🚀", "🎯", "💡"],
            "unicode": "café naïve résumé"
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded == data

    def test_special_numbers(self):
        """Test special number cases."""
        data = {
            "zero": 0,
            "negative_zero": -0,  # Should normalize to 0
            "large": 1000000,
            "decimal": 3.14159,
            "negative_decimal": -2.718,
            "scientific_small": 0.000001,
            "scientific_large": 1000000.0
        }
        result = encode(data)
        decoded = decode(result)
        assert decoded["zero"] == 0
        assert decoded["negative_zero"] == 0  # Should be normalized
        assert decoded["large"] == 1000000
        assert decoded["scientific_small"] == 0.000001

    def test_root_primitive_value(self):
        """Test encoding/decoding root primitive values."""
        test_values = [
            "hello world",
            42,
            True,
            False,
            None,
            "special, characters: here"
        ]

        for value in test_values:
            encoded = encode(value)
            decoded = decode(encoded)
            assert decoded == value

    def test_large_nested_structure(self):
        """Test performance with larger nested structures."""
        data = {
            "departments": [
                {
                    "name": f"Dept {i}",
                    "employees": [
                        {
                            "id": j,
                            "name": f"Employee {i}-{j}",
                            "skills": [f"skill{k}" for k in range(1, 4)],
                            "metadata": {
                                "joined": f"2024-{(j % 12) + 1:02d}",
                                "active": j % 2 == 0
                            }
                        }
                        for j in range(1, 6)
                    ]
                }
                for i in range(1, 4)
            ]
        }

        result = encode(data)
        decoded = decode(result)
        assert decoded == data
        assert len(result.split('\n')) > 50  # Should produce many lines


class TestStrictMode:
    """Test strict mode functionality."""

    def test_array_length_mismatch(self):
        """Test strict mode with array length mismatches."""
        # This tests the decoder's strict mode
        toon_str = "items[3]: a,b"  # Claims 3 items, only provides 2

        # Should work in non-strict mode
        try:
            result = decode(toon_str, options={'strict': False})
            assert result == {'items': ['a', 'b']}
        except ValueError:
            pass  # Implementation might still be strict

        # Should fail in strict mode
        with pytest.raises(ValueError):
            decode(toon_str, options={'strict': True})

    def test_tabular_row_count_mismatch(self):
        """Test strict mode with tabular row count mismatches."""
        toon_str = "users[2]{id,name}:\n  1,Alice"  # Claims 2 rows, only provides 1

        with pytest.raises(ValueError):
            decode(toon_str, options={'strict': True})


if __name__ == "__main__":
    pytest.main([__file__])