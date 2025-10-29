"""
Public encoder API for the Python TOON port.

The implementation mirrors the behaviour of the TypeScript reference encoder so
that downstream tooling can rely on identical output.
"""

from typing import Any, Optional

from .constants import DELIMITERS, DEFAULT_DELIMITER
from .encoders import encode_value
from .normalize import normalize_value
from .types import ResolvedEncodeOptions


def encode(input_value: Any, options: Optional[dict] = None, **kwargs) -> str:
    """
    Encode a Python value to TOON format.
    
    Args:
        input_value: Any JSON-serialisable value.
        options: Optional dict with keys:
            - indent: spaces per indentation level (default 2)
            - delimiter: 'comma' | 'tab' | 'pipe' | literal delimiter character
            - length_marker: '#' or False to toggle array length markers
    """
    merged_options = {**(options or {}), **kwargs}
    normalized = normalize_value(input_value)
    resolved = resolve_encode_options(merged_options)
    return encode_value(normalized, resolved)


def resolve_encode_options(options: Optional[dict]) -> ResolvedEncodeOptions:
    """Resolve raw user options into a ResolvedEncodeOptions instance."""
    opts = options or {}

    indent = int(opts.get('indent', 2))

    delimiter_option = opts.get('delimiter', DEFAULT_DELIMITER)
    delimiter = _normalise_delimiter(delimiter_option)

    length_marker_option = opts.get('length_marker', opts.get('lengthMarker', False))
    length_marker = _normalise_length_marker(length_marker_option)

    return ResolvedEncodeOptions(
        indent=indent,
        delimiter=delimiter,
        length_marker=length_marker,
    )


def _normalise_delimiter(value: Any) -> str:
    """Return a validated delimiter value (one of ',', '\\t', '|')."""
    if isinstance(value, str):
        lowered = value.lower()
        if lowered in DELIMITERS:
            return DELIMITERS[lowered]  # type: ignore[index]
        if value in DELIMITERS.values():
            return value
        if len(value) == 1 and value in (',', '\t', '|'):
            return value
    raise ValueError(f"Unsupported delimiter value: {value!r}")


def _normalise_length_marker(value: Any) -> str | bool:
    """Normalise the length marker option to '#' or False."""
    if value in (False, None):
        return False
    if value is True or value == '#':
        return '#'
    raise ValueError(f"Unsupported length_marker value: {value!r}")
