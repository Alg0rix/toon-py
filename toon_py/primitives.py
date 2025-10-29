"""
Primitive value encoding and formatting helpers.

This module mirrors the rules implemented in the TypeScript reference so that
string quoting, key encoding, and header formatting behave identically.
"""

import re
from typing import Iterable, Optional

from .constants import (
    BACKSLASH,
    COMMA,
    DEFAULT_DELIMITER,
    DOUBLE_QUOTE,
    ESCAPE_SEQUENCES,
    FALSE_LITERAL,
    LIST_ITEM_MARKER,
    NULL_LITERAL,
    TRUE_LITERAL,
)
from .types import JsonPrimitive


def encode_primitive(value: JsonPrimitive, delimiter: str | None = None) -> str:
    """Encode a single primitive value."""
    if value is None:
        return NULL_LITERAL
    if isinstance(value, bool):
        return TRUE_LITERAL if value else FALSE_LITERAL
    if isinstance(value, (int, float)):
        return str(value)
    return encode_string_literal(value, delimiter or DEFAULT_DELIMITER)


def encode_string_literal(value: str, delimiter: str = COMMA) -> str:
    """Encode a string literal, quoting only when required."""
    if is_safe_unquoted(value, delimiter):
        return value
    return f'{DOUBLE_QUOTE}{escape_string(value)}{DOUBLE_QUOTE}'


def escape_string(value: str) -> str:
    """Escape characters that require backslash sequences."""
    escaped = value
    for char, replacement in ESCAPE_SEQUENCES.items():
        escaped = escaped.replace(char, replacement)
    return escaped


def is_safe_unquoted(value: str, delimiter: str = COMMA) -> bool:
    """Return True if a string can remain unquoted according to the spec."""
    if not value:
        return False
    if value != value.strip():
        return False
    if value in (TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL):
        return False
    if is_numeric_like(value):
        return False
    if ':' in value or '"' in value or '\\' in value:
        return False
    if re.search(r'[\[\]{}]', value):
        return False
    if re.search(r'[\n\r\t]', value):
        return False
    if delimiter == '|':
        # Allow pipe characters when pipe is the active delimiter
        pass
    else:
        if delimiter in value:
            return False
        if '|' in value:
            return False
    if value.startswith(LIST_ITEM_MARKER):
        return False
    return True


def is_numeric_like(value: str) -> bool:
    """True when a string matches numeric literal patterns."""
    return bool(
        re.fullmatch(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?', value, flags=re.IGNORECASE)
        or re.fullmatch(r'0\d+', value)
    )


def encode_key(key: str) -> str:
    """Encode an object key, quoting only when necessary."""
    if re.fullmatch(r'[A-Za-z_][\w.]*', key):
        return key
    return f'{DOUBLE_QUOTE}{escape_string(key)}{DOUBLE_QUOTE}'


def encode_and_join_primitives(values: Iterable[JsonPrimitive], delimiter: str = COMMA) -> str:
    """Encode several primitive values and join them using the active delimiter."""
    return delimiter.join(encode_primitive(value, delimiter) for value in values)


def format_header(
    length: int,
    *,
    key: Optional[str] = None,
    fields: Optional[list[str]] = None,
    delimiter: str = DEFAULT_DELIMITER,
    length_marker: Optional[str | bool] = False,
) -> str:
    """
    Format an array or table header segment.
    
    The implementation mirrors the TypeScript formatter so that delimiters and
    optional field lists are emitted identically.
    """
    header = ''

    if key is not None:
        header += encode_key(key)

    marker = length_marker or ''
    suffix = delimiter if delimiter != DEFAULT_DELIMITER else ''
    header += f'[{marker}{length}{suffix}]'

    if fields:
        encoded_fields = [encode_key(field) for field in fields]
        header += '{' + delimiter.join(encoded_fields) + '}'

    header += ':'
    return header
