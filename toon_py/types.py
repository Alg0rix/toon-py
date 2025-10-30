"""
Type definitions for TOON.

This module mirrors the JSON data model and option types from the original
TypeScript reference implementation so that higher-level code can stay close
to the source material.
"""

from typing import Dict, List, Optional, Union, Literal

from .constants import DEFAULT_DELIMITER, Delimiter

# Core JSON types
JsonPrimitive = Union[str, int, float, bool, None]
JsonObject = Dict[str, 'JsonValue']
JsonArray = List['JsonValue']
JsonValue = Union[JsonPrimitive, JsonObject, JsonArray]

# Depth type for indentation tracking
Depth = int

# Sentinel type for length markers (keeps typing clear)
LiteralHash = Literal['#']

# Encoder options dictionary form (matches public API style)
EncodeOptions = Dict[str, Optional[Union[int, Delimiter, LiteralHash, bool]]]

# Decoder options dictionary form
DecodeOptions = Dict[str, Optional[Union[int, bool]]]


class ResolvedEncodeOptions:
    """Resolved encoder options with defaults applied."""
    
    indent: int
    delimiter: Delimiter
    lengthMarker: Union[LiteralHash, bool]
    
    def __init__(
        self,
        indent: int = 2,
        delimiter: Delimiter = DEFAULT_DELIMITER,
        length_marker: Union[LiteralHash, bool] = False,
    ):
        self.indent = indent
        self.delimiter = delimiter
        self.lengthMarker = length_marker


class ResolvedDecodeOptions:
    """Resolved decoder options with defaults applied."""
    
    indent: int
    strict: bool
    
    def __init__(self, indent: int = 2, strict: bool = True):
        self.indent = indent
        self.strict = strict


class ArrayHeaderInfo:
    """Information about an array header for decoding."""
    
    key: Optional[str]
    length: int
    delimiter: Delimiter
    fields: Optional[List[str]]
    hasLengthMarker: bool
    
    def __init__(
        self,
        key: Optional[str] = None,
        length: int = 0,
        delimiter: Delimiter = DEFAULT_DELIMITER,
        fields: Optional[List[str]] = None,
        hasLengthMarker: bool = False,
    ):
        self.key = key
        self.length = length
        self.delimiter = delimiter
        self.fields = fields
        self.hasLengthMarker = hasLengthMarker


class ParsedLine:
    """A line parsed from TOON text with depth and content information."""
    
    raw: str
    depth: int
    indent: int
    content: str
    
    def __init__(self, raw: str, depth: int, indent: int, content: str):
        self.raw = raw
        self.depth = depth
        self.indent = indent
        self.content = content
