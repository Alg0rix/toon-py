#!/usr/bin/env python3
"""
LLM Integration Examples.

This file demonstrates how to use TOON for LLM prompts,
showing token efficiency and structured data handling.
"""

from toon_py import encode, decode
import json


def main():
    print("🤖 TOON Python - LLM Integration Examples")
    print("=" * 50)

    # Example 1: Structured data for LLM context
    print("\n1. Structured Data for LLM Context:")

    user_profiles = {
        "users": [
            {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@company.com",
                "department": "Engineering",
                "skills": ["Python", "Machine Learning", "Docker"],
                "experience_years": 5,
                "active": True,
                "last_login": "2025-01-28T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "email": "bob@company.com",
                "department": "Design",
                "skills": ["Figma", "Sketch", "CSS"],
                "experience_years": 3,
                "active": True,
                "last_login": "2025-01-27T15:45:00Z"
            },
            {
                "id": 3,
                "name": "Carol Davis",
                "email": "carol@company.com",
                "department": "Product",
                "skills": ["Agile", "JIRA", "Analytics"],
                "experience_years": 7,
                "active": False,
                "last_login": "2025-01-20T09:15:00Z"
            }
        ]
    }

    json_context = json.dumps(user_profiles, indent=2)
    toon_context = encode(user_profiles)

    print("JSON format:")
    print(json_context[:400] + "..." if len(json_context) > 400 else json_context)
    print(f"Length: {len(json_context)} characters")

    print("\nTOON format:")
    print(toon_context[:400] + "..." if len(toon_context) > 400 else toon_context)
    print(f"Length: {len(toon_context)} characters")
    print(f"Token savings: {((len(json_context) - len(toon_context)) / len(json_context) * 100):.1f}%")

    # Example 2: Creating LLM prompts with TOON
    print("\n\n2. Creating LLM Prompts with TOON:")

    def create_llm_prompt(data, question):
        """Create an LLM prompt with TOON data."""
        toon_data = encode(data)
        prompt = f"""You are an AI assistant helping with data analysis.

Here is the data in TOON format:

```toon
{toon_data}
```

Question: {question}

Please analyze the data and provide a concise answer."""
        return prompt

    # Sample prompt
    prompt = create_llm_prompt(
        user_profiles,
        "Which active users have Machine Learning skills and how many years of experience do they have?"
    )

    print("Sample LLM prompt:")
    print(prompt[:600] + "..." if len(prompt) > 600 else prompt)

    # Example 3: Different data scenarios for LLMs
    print("\n\n3. Different Data Scenarios for LLMs:")

    # Analytics data
    analytics_data = {
        "metrics": [
            {"date": "2025-01-01", "page_views": 15420, "unique_visitors": 3420, "bounce_rate": 0.35, "avg_session_duration": 185},
            {"date": "2025-01-02", "page_views": 16890, "unique_visitors": 3850, "bounce_rate": 0.32, "avg_session_duration": 220},
            {"date": "2025-01-03", "page_views": 14230, "unique_visitors": 3120, "bounce_rate": 0.38, "avg_session_duration": 165},
            {"date": "2025-01-04", "page_views": 17890, "unique_visitors": 4100, "bounce_rate": 0.29, "avg_session_duration": 245}
        ]
    }

    print("Website Analytics Data:")
    analytics_toon = encode(analytics_data)
    print(analytics_toon)

    # Product catalog
    product_catalog = {
        "products": [
            {"sku": "LAP-001", "name": "Pro Laptop", "category": "Electronics", "price": 1299.99, "stock": 45, "rating": 4.5},
            {"sku": "MOU-002", "name": "Wireless Mouse", "category": "Electronics", "price": 49.99, "stock": 120, "rating": 4.2},
            {"sku": "CHA-003", "name": "Office Chair", "category": "Furniture", "price": 299.99, "stock": 15, "rating": 4.7},
            {"sku": "DES-004", "name": "Standing Desk", "category": "Furniture", "price": 599.99, "stock": 8, "rating": 4.8}
        ]
    }

    print("\nProduct Catalog Data:")
    catalog_toon = encode(product_catalog)
    print(catalog_toon)

    # Example 4: Parsing LLM responses back from TOON
    print("\n\n4. Parsing LLM Responses from TOON:")

    # Simulate LLM response in TOON format
    llm_response_toon = """recommendations[3]{product,reason,priority}:
  LAP-001,"High performance suitable for power users",High
  CHA-003,"Ergonomic design for long work sessions",Medium
  MOU-002,"Essential accessory for productivity",Low"""

    print("Simulated LLM response in TOON:")
    print(llm_response_toon)

    try:
        parsed_response = decode(llm_response_toon)
        print("\nParsed back to Python:")
        print(parsed_response)
    except Exception as e:
        print(f"\nError parsing: {e}")

    # Example 5: Token counting demonstration
    print("\n\n5. Token Efficiency Demonstration:")

    test_datasets = {
        "small": {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]},
        "medium": {"orders": [{"id": i, "customer": f"Cust {i}", "amount": (i*100)%1000+50, "items": (i%5)+1} for i in range(1, 11)]},
        "large": {"events": [{"timestamp": f"2025-01-{(i%28)+1:02d}T{(i%24):02d}:00:00Z", "type": ["click", "view", "purchase"][i%3], "user_id": (i%100)+1, "value": (i*17)%1000} for i in range(1, 51)]}
    }

    print("Dataset size comparison:")
    for name, data in test_datasets.items():
        json_len = len(json.dumps(data, separators=(',', ':')))
        toon_len = len(encode(data))
        savings = ((json_len - toon_len) / json_len * 100)

        print(f"{name.capitalize():7}: JSON {json_len:4} chars, TOON {toon_len:4} chars ({savings:5.1f}% smaller)")

    print("\n" + "=" * 50)
    print("✅ All LLM integration examples completed!")
    print("\n💡 Tips for LLM integration:")
    print("- Use TOON for structured data in prompts to reduce token usage")
    print("- Tabular format works best for uniform objects (arrays of objects with same fields)")
    print("- Consider using tab delimiters for data containing commas")
    print("- Include format examples in your prompts for better LLM understanding")
    print("- Use length markers to help LLMs track array sizes")


if __name__ == "__main__":
    main()