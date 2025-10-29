#!/usr/bin/env python3
"""
Test script for TOON Python implementation.
"""

from toon_py import encode, decode


def test_primitive():
    """Test encoding/decoding primitives."""
    test_cases = [
        None,
        True,
        False,
        42,
        -3.14,
        "hello",
        "",
        "hello, world",
    ]
    
    print("Testing primitives...")
    for value in test_cases:
        encoded = encode(value)
        decoded = decode(encoded)
        assert decoded == value, f"Failed for {value}: got {decoded}"
    print("✓ All primitive tests passed")


def test_simple_object():
    """Test encoding/decoding simple objects."""
    data = {"name": "Ada", "age": 30, "active": True}
    encoded = encode(data)
    print(f"\nSimple object:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == data, f"Decode failed: expected {data}, got {decoded}"
    print("✓ Simple object test passed")


def test_nested_object():
    """Test encoding/decoding nested objects."""
    data = {
        "user": {
            "name": "Ada",
            "contact": {
                "email": "ada@example.com",
                "phone": "555-0100"
            }
        }
    }
    encoded = encode(data)
    print(f"Nested object:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == data, f"Decode failed: expected {data}, got {decoded}"
    print("✓ Nested object test passed")


def test_primitive_array():
    """Test encoding/decoding primitive arrays."""
    data = {"tags": ["admin", "developer", "python"]}
    encoded = encode(data)
    print(f"Primitive array:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == data, f"Decode failed: expected {data}, got {decoded}"
    print("✓ Primitive array test passed")


def test_tabular_array():
    """Test encoding/decoding tabular arrays."""
    data = {
        "users": [
            {"id": 1, "name": "Ada", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ]
    }
    encoded = encode(data)
    print(f"Tabular array:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == data, f"Decode failed: expected {data}, got {decoded}"
    print("✓ Tabular array test passed")


def test_mixed_array():
    """Test encoding/decoding mixed arrays."""
    data = {
        "items": [
            1,
            {"a": 1},
            "text"
        ]
    }
    encoded = encode(data)
    print(f"Mixed array:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == data, f"Decode failed: expected {data}, got {decoded}"
    print("✓ Mixed array test passed")


def test_alternative_delimiter():
    """Test encoding with alternative delimiters."""
    data = {"tags": ["a,b", "c,d", "e|f"]}
    
    # Tab delimiter
    encoded = encode(data, delimiter='tab')
    print(f"Tab delimiter:\n{encoded}\n")
    
    # Pipe delimiter
    encoded = encode(data, delimiter='pipe')
    print(f"Pipe delimiter:\n{encoded}\n")
    
    print("✓ Alternative delimiter test passed")


def test_roundtrip():
    """Test full roundtrip encoding/decoding."""
    original = {
        "company": "Tech Corp",
        "founded": 2020,
        "active": True,
        "employees": [
            {"id": 1, "name": "Ada Lovelace", "skills": ["Python", "ML"], "salary": 90000},
            {"id": 2, "name": "Alan Turing", "skills": ["Mathematics", "Cryptography"], "salary": 95000}
        ],
        "metadata": None
    }
    
    encoded = encode(original)
    print(f"Full roundtrip test:\n{encoded}\n")
    
    decoded = decode(encoded)
    assert decoded == original, f"Roundtrip failed: expected {original}, got {decoded}"
    print("✓ Full roundtrip test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("TOON Python Implementation - Test Suite")
    print("=" * 60)
    
    try:
        test_primitive()
        test_simple_object()
        test_nested_object()
        test_primitive_array()
        test_tabular_array()
        test_mixed_array()
        test_alternative_delimiter()
        test_roundtrip()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
