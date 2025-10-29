# TOON Python Implementation

A Python implementation of **TOON (Token-Oriented Object Notation)** - a token-efficient JSON alternative for LLM prompts, following the original [@byjohann/toon](https://github.com/johannschopplich/toon) TypeScript/JavaScript implementation.

This implementation adheres to the [TOON v1.1 specification](https://github.com/johannschopplich/toon/blob/main/SPEC.md) and maintains compatibility with the original implementation.

## Features

- ✅ **Token-efficient**: 30-60% fewer tokens than JSON
- ✅ **LLM-friendly**: Explicit lengths and field lists help models validate output
- ✅ **Minimal syntax**: Removes redundant punctuation (braces, brackets, most quotes)
- ✅ **Indentation-based**: Uses whitespace for structure (like YAML)
- ✅ **Tabular arrays**: Declare keys once, stream rows without repetition
- ✅ **Spec-compliant**: Follows TOON v1.1 specification
- ✅ **Compatible**: Works with original TypeScript implementation

## Installation

```bash
uv add pytoon-core
```

or

```bash
pip install pytoon-core
```

Or install from source:

```bash
git clone https://github.com/Alg0rix/toon-py.git
cd toon-py
uv sync
```

## Quick Start

```python
from toon_py import encode, decode

# Encode Python values to TOON
data = {
    "name": "Ada",
    "age": 30,
    "active": True,
    "tags": ["admin", "developer", "python"]
}

toon_str = encode(data)
print(toon_str)
# Output:
# name: Ada
# age: 30
# active: true
# tags[3]: admin,developer,python

# Decode TOON back to Python
decoded = decode(toon_str)
print(decoded)
# Output:
# {'name': 'Ada', 'age': 30, 'active': True, 'tags': ['admin', 'developer', 'python']}
```

## Advanced Usage

### Tabular Arrays (Most Efficient)

When you have arrays of objects with the same structure, TOON uses an efficient tabular format:

```python
data = {
    "users": [
        {"id": 1, "name": "Ada", "role": "admin"},
        {"id": 2, "name": "Bob", "role": "user"},
        {"id": 3, "name": "Charlie", "role": "user"}
    ]
}

toon_str = encode(data)
print(toon_str)
# Output:
# users[3]{id,name,role}:
#   1,Ada,admin
#   2,Bob,user
#   3,Charlie,user
```

### Alternative Delimiters

Use tabs or pipes for even better token efficiency:

```python
# Tab delimiter
toon_str = encode(data, delimiter='tab')
print(toon_str)
# Output:
# users[3 ]{id name role}:
#   1 Ada admin
#   2 Bob user
#   3 Charlie user

# Pipe delimiter
toon_str = encode(data, delimiter='pipe')
print(toon_str)
# Output:
# users[3|]{id|name|role}:
#   1|Ada|admin
#   2|Bob|user
#   3|Charlie|user
```

### Nested Structures

TOON handles nested objects and arrays naturally:

```python
data = {
    "company": "Tech Corp",
    "employees": [
        {
            "name": "Ada",
            "contact": {"email": "ada@tech.com", "phone": "555-0101"},
            "skills": ["Python", "ML", "Data Science"]
        },
        {
            "name": "Bob",
            "contact": {"email": "bob@tech.com", "phone": "555-0102"},
            "skills": ["JavaScript", "React", "Node.js"]
        }
    ]
}

toon_str = encode(data)
print(toon_str)
# Output:
# company: Tech Corp
# employees[2]:
#   - name: Ada
#     contact:
#       email: ada@tech.com
#       phone: 555-0101
#     skills[3]: Python,ML,Data Science
#   - name: Bob
#     contact:
#       email: bob@tech.com
#       phone: 555-0102
#     skills[3]: JavaScript,React,Node.js
```

### Encoding Options

```python
encode(data, options={
    'indent': 2,           # Spaces per indent level (default: 2)
    'delimiter': ',',      # 'comma', 'tab', 'pipe', or actual char (default: ',')
    'length_marker': False  # Add '#' prefix to array lengths (default: False)
})
```

### Decoding Options

```python
decode(toon_str, options={
    'indent': 2,   # Expected indent size (default: 2)
    'strict': True # Strict validation (default: True)
})
```

## Format Comparison

### JSON (Verbose)

```json
{
  "users": [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"}
  ]
}
```

### TOON (Compact)

```
users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user
```

**Token savings**: ~40-50% fewer tokens than JSON!

## API Reference

### `encode(value, options=None)`

Encode a Python value to TOON format.

**Parameters:**

- `value`: Any JSON-serializable value (dict, list, or primitive)
- `options` (optional): Encoding options dict
  - `indent` (int): Spaces per indentation level (default: 2)
  - `delimiter` (str): Array delimiter - 'comma', 'tab', 'pipe', or the char (default: ',')
  - `length_marker` (bool): Prefix array lengths with '#' (default: False)

**Returns:** TOON-formatted string

### `decode(text, options=None)`

Decode TOON text to a Python value.

**Parameters:**

- `text`: TOON-formatted string
- `options` (optional): Decoding options dict
  - `indent` (int): Expected indent size (default: 2)
  - `strict` (bool): Enable strict validation (default: True)

**Returns:** Python value (dict, list, or primitive)

**Raises:**

- `ValueError`: If input is malformed or validation fails (in strict mode)

## Type Handling

The encoder automatically handles Python-specific types:

| Python Type | TOON Output |
|-------------|-------------|
| `int`, `float` | Number (normalized, no scientific notation) |
| `bool` | `true`/`false` |
| `None` | `null` |
| `str` | String (quoted if needed) |
| `datetime` | ISO 8601 string |
| `set` | Array |
| `dict` | Object |
| `list`, `tuple` | Array |
| `float('nan')`, `float('inf')` | `null` |
| `Decimal` | String (if outside safe integer range) |

## Whitespace Rules

TOON follows strict whitespace invariants:

- No trailing spaces on any line
- No trailing newline at end of document
- One space after `:` in key-value pairs
- Consistent indentation (configurable, default 2 spaces)

## Why TOON?

TOON is designed for **passing structured data to LLMs** with minimal token usage. While JSON is a great general-purpose format, it's verbose and token-expensive when used with LLMs. TOON solves this by:

1. **Removing redundant syntax** - No quotes on unquoted strings, no braces for objects
2. **Using tabular format** - For arrays of uniform objects, declare fields once
3. **Explicit lengths** - Help LLMs track array bounds
4. **Deterministic formatting** - Always produces the same output for the same input

## Compatibility

This Python implementation is designed to be compatible with the original TypeScript/JavaScript implementation. TOON documents encoded with this library can be decoded by the original library, and vice versa.

## Specification

This implementation follows the [TOON v1.1 Specification](https://github.com/johannschopplich/toon/blob/main/SPEC.md), which defines:

- Data model (JSON-compatible)
- Encoding normalization rules
- Concrete syntax
- Decoding semantics
- Conformance requirements

## Examples

See the `examples/` directory for comprehensive usage examples:

- **[basic_usage.py](./examples/basic_usage.py)** - Core functionality demonstration
- **[advanced_features.py](./examples/advanced_features.py)** - Advanced TOON features
- **[llm_integration.py](./examples/llm_integration.py)** - LLM integration scenarios
- **[performance_comparison.py](./examples/performance_comparison.py)** - Performance benchmarking

## Testing

The project includes a comprehensive test suite covering all TOON v1.1 specification features:

```bash
# Run all tests
uv run pytest tests/

# Run tests with coverage
uv run pytest tests/ --cov=toon_py --cov-report=html

# Run specific test categories
uv run pytest tests/test_basic_encoding.py     # Core functionality
uv run pytest tests/test_tabular_arrays.py     # Tabular format
uv run pytest tests/test_advanced_features.py  # Advanced features
uv run pytest tests/test_normalization.py      # Data normalization
```

### Test Coverage

- ✅ **Core TOON Features** - Primitives, objects, arrays, nesting
- ✅ **Tabular Optimization** - Uniform object arrays
- ✅ **Advanced Features** - Alternative delimiters, length markers
- ✅ **Edge Cases** - Unicode, special characters, large data
- ✅ **Normalization** - Python type handling
- ✅ **Compliance** - TOON v1.1 specification
- ✅ **Compatibility** - Reference implementation compatibility

## Benchmarks

TOON typically achieves 30-60% token reduction compared to JSON, depending on the data structure. See the [original benchmarks](https://github.com/johannschopplich/toon#benchmarks) for detailed comparisons.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please read the contributing guidelines and ensure all tests pass.

## Acknowledgments

- Original implementation by [Johann Schopplich](https://github.com/johannschopplich)
- Specification based on [TOON v1.1](https://github.com/johannschopplich/toon/blob/main/SPEC.md)
- Python port following the original TypeScript/JavaScript implementation

---

**Note**: TOON is designed for LLM input (passing data to models), not as a general-purpose serialization format like JSON. For APIs, databases, and other applications, JSON is still the better choice.
