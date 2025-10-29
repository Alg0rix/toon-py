"""
TOON decoder API.

This module provides the main decode() function for converting TOON text to Python values.
"""

from typing import Optional

from .types import ResolvedDecodeOptions, JsonValue
from .scanner import to_parsed_lines, LineCursor
from .decoders import decode_value_from_lines


def decode(
    input_text: str,
    options: Optional[dict] = None,
    **kwargs,
) -> JsonValue:
    """
    Decode TOON text back to a Python value.
    
    Args:
        input_text: The TOON-formatted string to decode
        options: Optional decoding options:
            - indent: Number of spaces per indentation level (default: 2)
            - strict: Enable strict validation (default: True)
            
    Returns:
        A Python value (dict, list, or primitive)
        
    Raises:
        ValueError: If the input is invalid or malformed
        
    Examples:
        >>> decode('name: Ada\\nage: 30')
        {'name': 'Ada', 'age': 30}
        
        >>> decode('tags[3]: a,b,c')
        {'tags': ['a', 'b', 'c']}
        
        >>> decode('items[2]{id,name}:\\n  1,A\\n  2,B')
        {'items': [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}]}
    """
    if not input_text or not input_text.strip():
        return {}
    
    merged = {**(options or {}), **kwargs}
    resolved = resolve_decode_options(merged)
    
    # Parse lines
    lines = to_parsed_lines(input_text, resolved.indent)
    
    if len(lines) == 0:
        return {}
    
    # Create cursor and decode
    cursor = LineCursor(lines)
    return decode_value_from_lines(cursor, resolved)


def resolve_decode_options(options: Optional[dict]) -> ResolvedDecodeOptions:
    """
    Resolve decoding options with defaults.
    
    Args:
        options: Options dict or None
        
    Returns:
        Resolved options
    """
    if options is None:
        options = {}
    
    indent = options.get('indent', 2)
    strict = options.get('strict', True)
    
    return ResolvedDecodeOptions(
        indent=int(indent),
        strict=bool(strict)
    )
