# TOON Python Tests

This directory contains comprehensive tests for the TOON Python implementation, covering all aspects of the TOON v1.1 specification.

## Test Structure

### 📋 [test_basic_encoding.py](./test_basic_encoding.py)
**Core functionality tests**

- Primitive value encoding/decoding
- Simple and nested objects
- Primitive arrays
- Root arrays
- Escaping and special characters

### 📊 [test_tabular_arrays.py](./test_tabular_arrays.py)
**Tabular format optimization tests**

- Uniform object arrays (tabular format)
- Non-tabular fallback scenarios
- Different delimiter support
- Root-level tabular arrays

### 🚀 [test_advanced_features.py](./test_advanced_features.py)
**Advanced feature tests**

- Alternative delimiters (tab, pipe)
- Length markers
- Complex nested structures
- Edge cases and Unicode
- Strict mode validation

### 🔄 [test_normalization.py](./test_normalization.py)
**Data normalization tests**

- Numeric value handling (NaN, Infinity, negative zero)
- BigInt/large integer support
- DateTime normalization
- Collection conversion (sets to arrays)
- Special value handling (functions, classes)

## Running Tests

### Run All Tests
```bash
# From project root
python -m pytest tests/

# With verbose output
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=toon_py --cov-report=html
```

### Run Specific Test Files
```bash
# Basic encoding tests
python -m pytest tests/test_basic_encoding.py -v

# Tabular array tests
python -m pytest tests/test_tabular_arrays.py -v

# Advanced features
python -m pytest tests/test_advanced_features.py -v

# Normalization tests
python -m pytest tests/test_normalization.py -v
```

### Run Specific Test Cases
```bash
# Run specific test class
python -m pytest tests/test_basic_encoding.py::TestPrimitives -v

# Run specific test method
python -m pytest tests/test_basic_encoding.py::TestPrimitives::test_primitive_encoding -v
```

## Test Coverage

The test suite covers:

### ✅ Core TOON Features
- [x] Primitive types (string, number, boolean, null)
- [x] Objects (simple and nested)
- [x] Arrays (primitive, tabular, mixed)
- [x] Root-level arrays and objects
- [x] Special character escaping

### ✅ Advanced Features
- [x] Alternative delimiters (comma, tab, pipe)
- [x] Length markers (`#N` format)
- [x] Complex nested structures
- [x] Unicode and emoji support
- [x] Strict mode validation

### ✅ Edge Cases
- [x] Empty structures
- [x] Large nested data
- [x] Special numeric values (NaN, Infinity)
- [x] Collection normalization
- [x] Host language type normalization

## Fixtures and Utilities

### Common Fixtures
- `sample_user_data` - Complex user profile with nesting
- `sample_product_data` - Tabular product catalog data
- `sample_analytics_data` - Analytics metrics for tabular testing
- `special_characters_data` - Data with escaping requirements

### Helper Functions
- `assert_roundtrip(data, **options)` - Verify encode/decode roundtrip
- `assert_token_efficiency(data, min_savings=0)` - Verify TOON efficiency vs JSON

## Test Categories

### 1. **Unit Tests**
- Individual function testing
- Edge case validation
- Error handling

### 2. **Integration Tests**
- End-to-end encode/decode cycles
- Complex structure handling
- Feature interaction testing

### 3. **Compliance Tests**
- TOON v1.1 specification compliance
- Reference implementation compatibility
- Format correctness validation

### 4. **Performance Tests**
- Token efficiency verification
- Large dataset handling
- Memory usage validation

## Adding New Tests

When adding new features, follow this pattern:

```python
class TestNewFeature:
    """Test new feature functionality."""

    def test_basic_functionality(self):
        """Test basic feature operation."""
        # Test implementation
        pass

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test edge cases
        pass

    def test_roundtrip(self, sample_data):
        """Test roundtrip encoding/decoding."""
        assert_roundtrip(sample_data)
```

## Test Data

All test data should:
- Be self-contained in fixtures
- Cover realistic use cases
- Include edge cases and special characters
- Be well-documented with purpose

## Debugging Tests

For debugging failing tests:

```bash
# Run with debugging
python -m pytest tests/ -v -s --pdb

# Run specific failing test
python -m pytest tests/test_file.py::TestClass::test_method -v -s

# Show local variables on failure
python -m pytest tests/ --tb=long -v
```

## Continuous Integration

The tests are designed to run in CI environments:
- No external dependencies
- Fast execution
- Clear failure reporting
- Coverage metrics available

## Reference Implementation Compatibility

Tests validate compatibility with the original TypeScript implementation by:
- Testing against the same input/output pairs
- Following the TOON v1.1 specification exactly
- Including reference examples from the spec
- Verifying edge case handling matches reference behavior