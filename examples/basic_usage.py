#!/usr/bin/env python3
"""
Basic TOON usage examples.

This file demonstrates the core functionality of TOON Python implementation.
"""

from toon_py import encode, decode


def main():
    print("🎯 TOON Python - Basic Usage Examples")
    print("=" * 50)

    # Example 1: Simple object
    print("\n1. Simple Object:")
    user_data = {"name": "Ada Lovelace", "age": 30, "active": True}
    toon_output = encode(user_data)
    print("Python:", user_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    # Example 2: Primitive arrays
    print("\n2. Primitive Arrays:")
    tags_data = {"tags": ["python", "ai", "developer"]}
    toon_output = encode(tags_data)
    print("Python:", tags_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    # Example 3: Tabular arrays (uniform objects)
    print("\n3. Tabular Arrays (Uniform Objects):")
    employees_data = {
        "employees": [
            {"id": 1, "name": "Alice", "role": "Engineer", "salary": 75000},
            {"id": 2, "name": "Bob", "role": "Designer", "salary": 70000},
            {"id": 3, "name": "Charlie", "role": "Manager", "salary": 85000}
        ]
    }
    toon_output = encode(employees_data)
    print("Python:", employees_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    # Example 4: Nested structures
    print("\n4. Nested Structures:")
    company_data = {
        "company": "Tech Corp",
        "departments": [
            {
                "name": "Engineering",
                "head": {"name": "Alice", "title": "CTO"},
                "budget": 500000,
                "projects": ["Project A", "Project B"]
            },
            {
                "name": "Design",
                "head": {"name": "Bob", "title": "Design Lead"},
                "budget": 200000,
                "projects": ["UI Redesign"]
            }
        ]
    }
    toon_output = encode(company_data)
    print("Python:", company_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    # Example 5: Mixed arrays
    print("\n5. Mixed Arrays:")
    mixed_data = {
        "items": [
            "simple string",
            42,
            {"nested": "object"},
            ["array", "of", "strings"],
            None
        ]
    }
    toon_output = encode(mixed_data)
    print("Python:", mixed_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    # Example 6: Special characters and quoting
    print("\n6. Special Characters and Quoting:")
    special_data = {
        "message": "Hello, world! This has: special characters",
        "path": "C:\\Users\\Admin\\Documents",
        "quote": 'She said: "TOON is great!"',
        "list": ["item with, comma", "item with: colon", "normal item"]
    }
    toon_output = encode(special_data)
    print("Python:", special_data)
    print("TOON:")
    print(toon_output)
    print("Decoded:", decode(toon_output))

    print("\n" + "=" * 50)
    print("✅ All basic examples completed!")


if __name__ == "__main__":
    main()