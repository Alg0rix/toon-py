"""
Normalization of values to TOON-compatible types.

This module converts Python types to the JSON-compatible data model defined
by the TOON specification, handling special cases like BigInt, Date, etc.
"""

import math
from decimal import Decimal
from datetime import datetime
from typing import Any

from .types import JsonValue, JsonObject


def normalize_value(value: Any) -> JsonValue:
    """
    Normalize a Python value to a TOON-compatible type.
    
    Follows the rules defined in TOON specification Section 3:
    - Finite numbers are kept as-is (with -0 normalized to 0)
    - NaN and infinities become null
    - BigInt within safe range becomes int
    - BigInt outside safe range becomes string
    - Date objects become ISO strings
    - Sets and Maps are converted
    - Functions, symbols, undefined become null
    
    Args:
        value: The value to normalize
        
    Returns:
        A TOON-compatible value
    """
    # None/null
    if value is None:
        return None
    
    # Boolean
    if isinstance(value, bool):
        return value

    # Decimal support
    if isinstance(value, Decimal):
        if value.is_nan() or value.is_infinite():
            return None
        return float(value)

    # Numbers - check for non-finite values first (NaN, ±Infinity)
    if isinstance(value, (int, float)):
        if isinstance(value, float):
            if math.isnan(value) or math.isinf(value):
                return None
            # Normalize -0 to 0
            if value == 0 and str(value) == '-0.0':
                return 0
        return value
    
    # BigInt handling (Python 3.8+)
    try:
        if isinstance(value, int) and not isinstance(value, bool):
            # Check if it's within safe integer range
            if -2**53 <= value <= 2**53:
                return int(value)
            else:
                # Outside safe range, convert to string
                return str(value)
    except (AttributeError, TypeError):
        pass
    
    # String
    if isinstance(value, str):
        return value
    
    # Date/datetime - convert to ISO string
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Set - convert to array
    if isinstance(value, set):
        return [normalize_value(item) for item in value]
    
    # Dict/object - convert keys to strings recursively
    if isinstance(value, dict):
        result: JsonObject = {}
        for key, val in value.items():
            # Keys must be strings
            result[str(key)] = normalize_value(val)
        return result
    
    # List/tuple - convert to array
    if isinstance(value, (list, tuple)):
        return [normalize_value(item) for item in value]
    
    # Function, lambda, or other non-serializable types
    return None


def is_json_primitive(value: Any) -> bool:
    """Check if a value is a JSON primitive."""
    return value is None or isinstance(value, (str, int, float, bool))


def is_json_object(value: Any) -> bool:
    """Check if a value is a JSON object (dict)."""
    return isinstance(value, dict)


def is_json_array(value: Any) -> bool:
    """Check if a value is a JSON array (list)."""
    return isinstance(value, list)


def is_array_of_primitives(value: Any) -> bool:
    """Check if a value is an array containing only primitives."""
    if not isinstance(value, list):
        return False
    return all(is_json_primitive(item) for item in value)


def is_array_of_objects(value: Any) -> bool:
    """Check if a value is an array containing only objects."""
    if not isinstance(value, list):
        return False
    if len(value) == 0:
        return False
    return all(isinstance(item, dict) for item in value)


def is_array_of_arrays(value: Any) -> bool:
    """Check if a value is an array containing only arrays."""
    if not isinstance(value, list):
        return False
    if len(value) == 0:
        return False
    return all(isinstance(item, list) for item in value)
