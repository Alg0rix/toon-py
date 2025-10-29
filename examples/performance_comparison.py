#!/usr/bin/env python3
"""
Performance comparison between TOON and other formats.

This file demonstrates the token efficiency and performance benefits of TOON.
"""

import json
import time
from toon_py import encode, decode


def main():
    print("⚡ TOON Python - Performance Comparison")
    print("=" * 50)

    # Generate test datasets
    test_cases = generate_test_datasets()

    for name, data in test_cases.items():
        print(f"\n📊 {name.upper()} DATASET")
        print("-" * 30)

        # JSON encoding
        json_str = json.dumps(data, separators=(',', ':'))
        json_compact = len(json_str)

        # TOON encoding (default)
        toon_str = encode(data)
        toon_compact = len(toon_str)

        # TOON with tab delimiter
        toon_tab_str = encode(data, delimiter='tab')
        toon_tab_compact = len(toon_tab_str)

        # Calculate savings
        json_vs_toon = ((json_compact - toon_compact) / json_compact * 100)
        json_vs_tab = ((json_compact - toon_tab_compact) / json_compact * 100)

        print(f"JSON (compact):     {json_compact:6} characters")
        print(f"TOON (comma):       {toon_compact:6} characters ({json_vs_toon:5.1f}% smaller)")
        print(f"TOON (tab):         {toon_tab_compact:6} characters ({json_vs_tab:5.1f}% smaller)")

        # Performance test
        print("\n⏱️  Performance Test:")

        # JSON encoding/decoding
        json_encode_time = time_benchmark(lambda: json.dumps(data, separators=(',', ':')), iterations=1000)
        json_decode_time = time_benchmark(lambda: json.loads(json_str), iterations=1000)

        # TOON encoding/decoding
        toon_encode_time = time_benchmark(lambda: encode(data), iterations=1000)
        toon_decode_time = time_benchmark(lambda: decode(toon_str), iterations=1000)

        print(f"JSON encode: {json_encode_time*1000:6.2f}ms")
        print(f"JSON decode: {json_decode_time*1000:6.2f}ms")
        print(f"TOON encode: {toon_encode_time*1000:6.2f}ms")
        print(f"TOON decode: {toon_decode_time*1000:6.2f}ms")

        # Show sample output for smaller datasets
        if len(json_str) < 500:
            print("\nSample JSON:")
            print(json_str[:200] + "..." if len(json_str) > 200 else json_str)
            print("\nSample TOON:")
            print(toon_str[:200] + "..." if len(toon_str) > 200 else toon_str)

    # Overall summary
    print("\n📈 OVERALL SUMMARY")
    print("=" * 50)

    total_json = sum(len(json.dumps(data, separators=(',', ':'))) for data in test_cases.values())
    total_toon = sum(len(encode(data)) for data in test_cases.values())
    total_savings = ((total_json - total_toon) / total_json * 100)

    print(f"Total JSON characters:  {total_json}")
    print(f"Total TOON characters:  {total_toon}")
    print(f"Overall reduction:       {total_savings:.1f}%")

    print("\n💡 Key Benefits:")
    print(f"- Significant token reduction ({total_savings:.1f}% average)")
    print("- Better for LLM context windows")
    print("- More human-readable than compact JSON")
    print("- Structured format for easy parsing")


def generate_test_datasets():
    """Generate various test datasets for comparison."""

    return {
        "user_profiles": {
            "users": [
                {
                    "id": i,
                    "name": f"User {i}",
                    "email": f"user{i}@example.com",
                    "department": ["Engineering", "Design", "Marketing", "Sales"][i % 4],
                    "skills": [f"Skill {j}" for j in range(1, (i % 3) + 2)],
                    "active": i % 2 == 0,
                    "salary": 50000 + (i * 5000)
                }
                for i in range(1, 11)
            ]
        },

        "sales_data": {
            "sales": [
                {
                    "order_id": f"ORD-{1000 + i}",
                    "customer": f"Customer {i}",
                    "date": f"2025-01-{(i % 28) + 1:02d}",
                    "items": [
                        {"product": f"Product {j}", "quantity": (j * 2) % 5 + 1, "price": round((j * 19.99) + 9.99, 2)}
                        for j in range(1, (i % 3) + 2)
                    ],
                    "total": round((i * 123.45) + 50.0, 2),
                    "status": ["pending", "shipped", "delivered"][i % 3]
                }
                for i in range(1, 21)
            ]
        },

        "analytics_metrics": {
            "metrics": [
                {
                    "date": f"2025-01-{(i % 30) + 1:02d}",
                    "page_views": 10000 + (i * 500),
                    "unique_visitors": 2000 + (i * 100),
                    "bounce_rate": round(0.3 + (i % 10) * 0.02, 3),
                    "avg_session_duration": 120 + (i * 15),
                    "conversion_rate": round(0.02 + (i % 5) * 0.005, 4),
                    "revenue": round(500 + (i * 75.50), 2)
                }
                for i in range(1, 31)
            ]
        },

        "product_catalog": {
            "products": [
                {
                    "sku": f"SKU-{1000 + i}",
                    "name": f"Product {i}",
                    "category": ["Electronics", "Clothing", "Books", "Home", "Sports"][i % 5],
                    "price": round(10.0 + (i * 23.75), 2),
                    "description": f"This is a detailed description for product {i} with many features and benefits",
                    "tags": [f"tag{j}" for j in range(1, (i % 4) + 2)],
                    "in_stock": i % 3 != 0,
                    "rating": round(3.0 + (i % 20) * 0.1, 1),
                    "reviews_count": (i * 7) % 100
                }
                for i in range(1, 51)
            ]
        },

        "simple_primitives": {
            "settings": {
                "theme": ["dark", "light", "auto"][0],
                "notifications": True,
                "max_items": 100,
                "features": ["feature_a", "feature_b", "feature_c"],
                "version": "2.1.0",
                "debug": False,
                "timeout": 30.5,
                "languages": ["en", "es", "fr", "de", "ja"],
                "beta_features": []
            }
        }
    }


def time_benchmark(func, iterations=1000):
    """Benchmark a function's execution time."""
    start_time = time.perf_counter()

    for _ in range(iterations):
        func()

    end_time = time.perf_counter()
    return (end_time - start_time) / iterations


if __name__ == "__main__":
    main()