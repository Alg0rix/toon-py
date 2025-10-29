#!/usr/bin/env python3
"""
Advanced TOON features examples.

This file demonstrates advanced features like alternative delimiters,
length markers, and complex data structures.
"""

from toon_py import encode, decode


def main():
    print("🚀 TOON Python - Advanced Features")
    print("=" * 50)

    # Example 1: Alternative delimiters
    print("\n1. Alternative Delimiters:")
    data_with_commas = {
        "phrases": [
            "Hello, world!",
            "Good morning, everyone",
            "To be, or not to be"
        ]
    }

    print("Default comma delimiter:")
    toon_comma = encode(data_with_commas)
    print(toon_comma)

    print("\nTab delimiter (avoids quoting commas):")
    toon_tab = encode(data_with_commas, delimiter='tab')
    print(toon_tab)

    print("\nPipe delimiter:")
    toon_pipe = encode(data_with_commas, delimiter='pipe')
    print(toon_pipe)

    # Example 2: Length markers
    print("\n2. Length Markers:")
    array_data = {
        "metrics": [1.5, 2.3, 4.7, 3.2],
        "categories": ["A", "B", "C", "D", "E"]
    }

    print("Without length marker:")
    toon_no_marker = encode(array_data)
    print(toon_no_marker)

    print("\nWith length marker:")
    toon_with_marker = encode(array_data, length_marker=True)
    print(toon_with_marker)

    # Example 3: Complex nested structures
    print("\n3. Complex Nested Structures:")
    complex_data = {
        "analytics": {
            "period": "2025-01",
            "datasets": [
                {
                    "name": "user_metrics",
                    "data": [
                        {"date": "2025-01-01", "users": 1250, "sessions": 3400, "revenue": 1250.50},
                        {"date": "2025-01-02", "users": 1320, "sessions": 3650, "revenue": 1420.75},
                        {"date": "2025-01-03", "users": 1180, "sessions": 3100, "revenue": 980.25}
                    ]
                },
                {
                    "name": "performance_metrics",
                    "data": {
                        "response_times": [120, 135, 110, 145, 125],
                        "error_rates": [0.01, 0.02, 0.005, 0.015, 0.008],
                        "uptime_percentages": [99.9, 99.8, 99.95, 99.7, 99.85]
                    }
                }
            ]
        }
    }

    toon_complex = encode(complex_data)
    print("Python structure:")
    print(complex_data)
    print("\nTOON output:")
    print(toon_complex)

    # Verify roundtrip
    decoded = decode(toon_complex)
    print("\n✅ Roundtrip successful:", decoded == complex_data)

    # Example 4: Arrays of arrays
    print("\n4. Arrays of Arrays:")
    matrix_data = {
        "matrices": [
            [[1, 2, 3], [4, 5, 6]],
            [[7, 8, 9], [10, 11, 12]],
            [[13, 14, 15], [16, 17, 18]]
        ]
    }

    toon_matrix = encode(matrix_data)
    print("Python:", matrix_data)
    print("TOON:")
    print(toon_matrix)
    print("Decoded:", decode(toon_matrix))

    # Example 5: Empty structures and edge cases
    print("\n5. Empty Structures and Edge Cases:")
    edge_cases = {
        "empty_object": {},
        "empty_array": [],
        "nested_empty": {
            "empty_obj": {},
            "empty_arr": [],
            "mixed": [1, {}, "test", []]
        },
        "null_values": {
            "null_field": None,
            "mixed": [None, "text", None, 42]
        },
        "boolean_values": {
            "flags": [True, False, True],
            "settings": {
                "enabled": True,
                "debug": False
            }
        }
    }

    toon_edges = encode(edge_cases)
    print("Python:", edge_cases)
    print("TOON:")
    print(toon_edges)
    print("Decoded:", decode(toon_edges))

    # Example 6: Large tabular data (token efficiency demo)
    print("\n6. Large Tabular Data (Token Efficiency):")
    large_dataset = {
        "sales_data": [
            {"id": i, "product": f"Product {i%10+1}", "quantity": (i*7)%50+1, "price": round((i*13)%100+10.99, 2), "category": f"Category {chr(65+(i%5))}"}
            for i in range(1, 21)  # 20 rows
        ]
    }

    toon_large = encode(large_dataset)
    print(f"Generated {len(large_dataset['sales_data'])} rows")
    print("First few lines of TOON:")
    lines = toon_large.split('\n')[:10]
    for line in lines:
        print(line)
    print("...")

    # Token efficiency comparison
    import json
    json_str = json.dumps(large_dataset, separators=(',', ':'))
    print("\nToken comparison:")
    print(f"JSON:  {len(json_str)} characters")
    print(f"TOON:  {len(toon_large)} characters")
    print(f"Savings: {((len(json_str) - len(toon_large)) / len(json_str) * 100):.1f}% reduction")

    print("\n" + "=" * 50)
    print("✅ All advanced examples completed!")


if __name__ == "__main__":
    main()