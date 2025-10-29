# TOON Python Examples

This directory contains comprehensive examples demonstrating the TOON Python implementation's capabilities.

## Files Overview

### 📚 [basic_usage.py](./basic_usage.py)
**Core functionality demonstration**

- Simple object encoding/decoding
- Primitive arrays
- Tabular arrays (uniform objects)
- Nested structures
- Mixed arrays
- Special character handling

**Run:** `python basic_usage.py`

### 🚀 [advanced_features.py](./advanced_features.py)
**Advanced TOON features**

- Alternative delimiters (tab, pipe)
- Length markers
- Complex nested structures
- Arrays of arrays
- Empty structures and edge cases
- Large tabular data efficiency

**Run:** `python advanced_features.py`

### 🤖 [llm_integration.py](./llm_integration.py)
**LLM integration examples**

- Structured data for LLM context
- Token efficiency demonstration
- LLM prompt creation
- Different data scenarios
- Parsing LLM responses

**Run:** `python llm_integration.py`

### ⚡ [performance_comparison.py](./performance_comparison.py)
**Performance benchmarking**

- Character count comparisons (TOON vs JSON)
- Encoding/decoding performance
- Multiple dataset sizes
- Efficiency metrics
- Statistical analysis

**Run:** `python performance_comparison.py`

## Quick Start

To run all examples:

```bash
# Navigate to examples directory
cd examples

# Run each example
python basic_usage.py
python advanced_features.py
python llm_integration.py
python performance_comparison.py
```

## Key Features Demonstrated

### 1. **Token Efficiency**
TOON typically reduces character count by 30-60% compared to JSON:

```python
data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}

# JSON: ~80 characters
# TOON: ~50 characters (37% reduction)
```

### 2. **Tabular Format**
Perfect for uniform arrays of objects:

```python
employees[3]{id,name,role}:
  1,Alice,Engineer
  2,Bob,Designer
  3,Carol,Manager
```

### 3. **Alternative Delimiters**
Use tab or pipe delimiters for data containing commas:

```python
# Tab delimiter
phrases[3	]:
  Hello, world!
  Good morning, everyone
  To be, or not to be
```

### 4. **LLM Integration**
Ideal for structured data in LLM prompts:

```python
# Create efficient prompts
prompt = f"""
Data:
```toon
{encode(data)}
```

Question: {question}
"""
```

## TOON Syntax Quick Reference

| Structure | JSON | TOON |
|-----------|------|------|
| Object | `{"id": 1, "name": "Ada"}` | `id: 1\nname: Ada` |
| Nested Object | `{"user": {"id": 1}}` | `user:\n  id: 1` |
| Primitive Array | `{"tags": ["a","b"]}` | `tags[2]: a,b` |
| Tabular Array | Complex JSON | `items[2]{id,name}:\n  1,A\n  2,B` |
| Mixed Array | Various formats | `items[3]:\n  - 1\n  - a: 1\n  - text` |

## Benefits for LLM Integration

- **Reduced Token Usage**: 30-60% fewer tokens than JSON
- **Structured Format**: Easy for LLMs to parse and generate
- **Length Markers**: Help LLMs track array sizes
- **Tabular Optimization**: Efficient for uniform data
- **Delimiter Flexibility**: Choose optimal delimiters for your data

## Best Practices

1. **Use tabular format** for uniform objects (same fields, primitive values)
2. **Choose appropriate delimiters** based on your data content
3. **Include format examples** in LLM prompts
4. **Use length markers** for better LLM understanding
5. **Test roundtrip encoding/decoding** for your specific data structures

## Performance Tips

- TOON encoding is slightly slower than JSON due to format optimization
- TOON decoding is competitive with JSON parsing speed
- Character count reduction is the primary benefit, not CPU performance
- Use for LLM contexts where token efficiency matters more than CPU time