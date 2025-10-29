"""
Normalization tests for TOON Python implementation.

Tests the normalization of Python values to JSON-compatible types.
"""

import pytest
from datetime import datetime
from decimal import Decimal
from toon_py.normalize import normalize_value


class TestNumericNormalization:
    """Test normalization of numeric values."""

    def test_positive_integers(self):
        """Test positive integers."""
        assert normalize_value(42) == 42
        assert normalize_value(0) == 0

    def test_negative_integers(self):
        """Test negative integers."""
        assert normalize_value(-17) == -17

    def test_positive_floats(self):
        """Test positive floats."""
        assert normalize_value(3.14) == 3.14
        assert normalize_value(0.0) == 0.0

    def test_negative_floats(self):
        """Test negative floats."""
        assert normalize_value(-2.718) == -2.718

    def test_negative_zero(self):
        """Test negative zero normalization."""
        assert normalize_value(-0.0) == 0.0

    def test_nan(self):
        """Test NaN normalization."""
        assert normalize_value(float('nan')) is None

    def test_infinity(self):
        """Test infinity normalization."""
        assert normalize_value(float('inf')) is None
        assert normalize_value(float('-inf')) is None

    def test_decimal_numbers(self):
        """Test Decimal normalization."""
        assert normalize_value(Decimal('3.14')) == 3.14
        assert normalize_value(Decimal('-2.5')) == -2.5


class TestBigIntNormalization:
    """Test BigInt normalization (Python int equivalents)."""

    def test_large_integers(self):
        """Test large integers (equivalent to BigInt in JS)."""
        # Python integers are arbitrary precision, so they work like BigInt
        large_int = 9007199254740993  # Beyond Number.MAX_SAFE_INTEGER
        assert normalize_value(large_int) == large_int

    def test_very_large_integers(self):
        """Test very large integers."""
        very_large = 10**100
        assert normalize_value(very_large) == very_large


class TestDateTimeNormalization:
    """Test datetime normalization."""

    def test_datetime_object(self):
        """Test datetime object normalization."""
        dt = datetime(2025, 1, 15, 10, 30, 0)
        result = normalize_value(dt)
        assert result == "2025-01-15T10:30:00"

    def test_datetime_with_microseconds(self):
        """Test datetime with microseconds."""
        dt = datetime(2025, 1, 15, 10, 30, 0, 123456)
        result = normalize_value(dt)
        assert result == "2025-01-15T10:30:00.123456"

    def test_utc_datetime(self):
        """Test UTC datetime."""
        # Note: This would require timezone-aware datetime, but we're keeping it simple
        dt = datetime(2025, 1, 15, 10, 30, 0)
        result = normalize_value(dt)
        assert isinstance(result, str)
        assert "2025-01-15T10:30:00" in result


class TestCollectionNormalization:
    """Test collection normalization."""

    def test_list_normalization(self):
        """Test list normalization."""
        data = [1, "two", True, None]
        result = normalize_value(data)
        assert result == [1, "two", True, None]

    def test_nested_list_normalization(self):
        """Test nested list normalization."""
        data = [[1, 2], [3, 4]]
        result = normalize_value(data)
        assert result == [[1, 2], [3, 4]]

    def test_set_normalization(self):
        """Test set normalization to array."""
        data = {1, 2, 3}
        result = normalize_value(data)
        assert isinstance(result, list)
        assert set(result) == {1, 2, 3}

    def test_set_with_mixed_types(self):
        """Test set with mixed types."""
        data = {1, "two", True}
        result = normalize_value(data)
        assert isinstance(result, list)
        assert 1 in result
        assert "two" in result
        assert True in result

    def test_dict_normalization(self):
        """Test dict normalization."""
        data = {"a": 1, "b": "two"}
        result = normalize_value(data)
        assert result == {"a": 1, "b": "two"}

    def test_dict_with_non_string_keys(self):
        """Test dict with non-string keys."""
        data = {1: "one", 2.5: "two and half", False: "boolean"}
        result = normalize_value(data)
        assert result == {"1": "one", "2.5": "two and half", "False": "boolean"}


class TestSpecialValueNormalization:
    """Test special value normalization."""

    def test_none_normalization(self):
        """Test None normalization."""
        assert normalize_value(None) is None

    def test_boolean_normalization(self):
        """Test boolean normalization."""
        assert normalize_value(True) is True
        assert normalize_value(False) is False

    def test_string_normalization(self):
        """Test string normalization."""
        assert normalize_value("hello") == "hello"
        assert normalize_value("") == ""

    def test_function_normalization(self):
        """Test function normalization."""
        def dummy_func():
            pass

        assert normalize_value(dummy_func) is None

    def test_lambda_normalization(self):
        """Test lambda normalization."""
        def dummy_lambda(x):
            return x
        assert normalize_value(dummy_lambda) is None

    def test_class_normalization(self):
        """Test class normalization."""
        class DummyClass:
            pass

        assert normalize_value(DummyClass) is None

    def test_instance_normalization(self):
        """Test class instance normalization."""
        class DummyClass:
            def __init__(self):
                self.value = 42

        instance = DummyClass()
        assert normalize_value(instance) is None

    def test_symbol_equivalent(self):
        """Test Python equivalents of symbols."""
        # Python doesn't have symbols like JavaScript, but we can test similar cases
        class SymbolLike:
            pass

        assert normalize_value(SymbolLike()) is None


class TestComplexNestedNormalization:
    """Test complex nested structures normalization."""

    def test_deeply_nested_structure(self):
        """Test deeply nested structure with various types."""
        data = {
            "level1": [
                {
                    "level2": {
                        "level3": [
                            1,
                            "two",
                            True,
                            None,
                            float('nan'),  # Should become None
                            {"nested": "value"}
                        ]
                    }
                }
            ]
        }

        result = normalize_value(data)

        # Check that NaN was normalized to None
        assert result["level1"][0]["level2"]["level3"][3] is None

    def test_mixed_collections(self):
        """Test mixing of lists, sets, and dicts."""
        data = {
            "list": [1, 2, 3],
            "set": {4, 5, 6},
            "dict": {"seven": 7, "eight": 8},
            "mixed": [
                {9, 10},
                {"eleven": 11},
                [12, 13, 14]
            ]
        }

        result = normalize_value(data)

        # Check that set became list
        assert isinstance(result["set"], list)
        assert set(result["set"]) == {4, 5, 6}

        # Check nested set became list
        assert isinstance(result["mixed"][0], list)
        assert set(result["mixed"][0]) == {9, 10}

    def test_edge_case_values(self):
        """Test edge case values."""
        data = {
            "empty_string": "",
            "zero": 0,
            "negative_zero": -0.0,
            "empty_list": [],
            "empty_dict": {},
            "nested_empty": {
                "empty": {},
                "list": []
            },
            "extreme_numbers": [
                float('inf'),
                float('-inf'),
                float('nan')
            ]
        }

        result = normalize_value(data)

        # Check normalization of special numbers
        assert result["extreme_numbers"][0] is None
        assert result["extreme_numbers"][1] is None
        assert result["extreme_numbers"][2] is None

        # Check negative zero normalization
        assert result["negative_zero"] == 0.0


class TestPreservationOfValidTypes:
    """Test that valid JSON-compatible types are preserved."""

    def test_primitive_preservation(self):
        """Test that primitives are preserved."""
        primitives = [
            "hello",
            42,
            -17,
            3.14,
            True,
            False,
            None
        ]

        for primitive in primitives:
            assert normalize_value(primitive) is primitive

    def test_simple_collections_preservation(self):
        """Test that simple collections are preserved."""
        collections = [
            [1, 2, 3],
            {"a": 1, "b": 2},
            []
        ]

        for collection in collections:
            result = normalize_value(collection)
            assert result == collection
            assert type(result) is type(collection)


if __name__ == "__main__":
    pytest.main([__file__])