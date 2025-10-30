"""
Parser utilities mirroring the TypeScript implementation.

These helpers keep the decoding logic aligned with the canonical TOON parser,
handling array headers, delimited value parsing, and primitive interpretation.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from .constants import (
    BACKSLASH,
    CARRIAGE_RETURN,
    CLOSE_BRACE,
    CLOSE_BRACKET,
    COLON,
    DEFAULT_DELIMITER,
    DELIMITERS,
    DOUBLE_QUOTE,
    FALSE_LITERAL,
    HASH,
    NEWLINE,
    NULL_LITERAL,
    OPEN_BRACE,
    OPEN_BRACKET,
    PIPE,
    TAB,
    TRUE_LITERAL,
)
from .types import ArrayHeaderInfo, JsonPrimitive


def parse_array_header_line(
    content: str,
    default_delimiter: str = DEFAULT_DELIMITER,
) -> Optional[dict]:
    """
    Parse an array header line such as ``items[2]{id,name}:``.
    
    Returns a dictionary with ``header`` (ArrayHeaderInfo) and optional
    ``inlineValues`` matching the TypeScript reference.
    """
    if content.lstrip().startswith(DOUBLE_QUOTE):
        return None

    bracket_start = content.find(OPEN_BRACKET)
    if bracket_start == -1:
        return None

    bracket_end = content.find(CLOSE_BRACKET, bracket_start)
    if bracket_end == -1:
        return None

    colon_index = bracket_end + 1
    brace_end = colon_index

    brace_start = content.find(OPEN_BRACE, bracket_end)
    if brace_start != -1:
        colon_after_bracket = content.find(COLON, bracket_end)
        if colon_after_bracket != -1 and brace_start < colon_after_bracket:
            found_brace_end = content.find(CLOSE_BRACE, brace_start)
            if found_brace_end != -1:
                brace_end = found_brace_end + 1

    colon_index = content.find(COLON, max(bracket_end, brace_end))
    if colon_index == -1:
        return None

    key_segment = content[:bracket_start].strip() or None
    after_colon = content[colon_index + 1 :].strip()
    bracket_content = content[bracket_start + 1 : bracket_end]

    try:
        length, delimiter, has_length_marker = parse_bracket_segment(bracket_content, default_delimiter)
    except ValueError:
        return None

    fields: Optional[List[str]] = None
    if brace_start != -1 and brace_start < colon_index:
        found_brace_end = content.find(CLOSE_BRACE, brace_start)
        if found_brace_end != -1 and found_brace_end < colon_index:
            fields_segment = content[brace_start + 1 : found_brace_end]
            fields = parse_fields_segment(fields_segment, delimiter)

    key = None
    if key_segment is not None:
        if key_segment.startswith(DOUBLE_QUOTE):
            key = parse_string_literal(key_segment)
        else:
            key = key_segment

    return {
        'header': ArrayHeaderInfo(
            key=key,
            length=length,
            delimiter=delimiter,
            fields=fields,
            hasLengthMarker=has_length_marker,
        ),
        'inlineValues': after_colon or None,
    }


def parse_bracket_segment(segment: str, default_delimiter: str) -> Tuple[int, str, bool]:
    """Parse the inside of the ``[...`` portion of an array header."""
    has_length_marker = False
    content = segment

    if content.startswith(HASH):
        has_length_marker = True
        content = content[1:]

    delimiter = default_delimiter
    if content.endswith(TAB):
        delimiter = DELIMITERS['tab']
        content = content[:-1]
    elif content.endswith(PIPE):
        delimiter = DELIMITERS['pipe']
        content = content[:-1]

    if not content or not content.isdigit():
        raise ValueError(f'Invalid array length: {segment!r}')

    length = int(content, 10)
    return length, delimiter, has_length_marker


def parse_fields_segment(segment: str, delimiter: str) -> List[str]:
    """Parse the ``{a,b,c}`` portion of a tabular header."""
    return [parse_string_literal(field.strip()) for field in parse_delimited_values(segment, delimiter)]


def parse_delimited_values(input_text: str, delimiter: str) -> List[str]:
    """Split a row into raw cell strings, accounting for quotes and escapes."""
    values: List[str] = []
    current = ''
    in_quotes = False
    i = 0

    while i < len(input_text):
        char = input_text[i]

        if char == BACKSLASH and i + 1 < len(input_text) and in_quotes:
            current += char + input_text[i + 1]
            i += 2
            continue

        if char == DOUBLE_QUOTE:
            in_quotes = not in_quotes
            current += char
            i += 1
            continue

        if char == delimiter and not in_quotes:
            values.append(current.strip())
            current = ''
            i += 1
            continue

        current += char
        i += 1

    if current or values:
        values.append(current.strip())

    return values


def map_row_values_to_primitives(values: List[str]) -> List[JsonPrimitive]:
    """Convert raw row strings into JSON primitives."""
    return [parse_primitive_token(value) for value in values]


def parse_primitive_token(token: str) -> JsonPrimitive:
    """Parse a primitive token (string, number, boolean, null)."""
    trimmed = token.strip()
    if not trimmed:
        return ''

    if trimmed.startswith(DOUBLE_QUOTE):
        return parse_string_literal(trimmed)

    if is_boolean_or_null_literal(trimmed):
        if trimmed == TRUE_LITERAL:
            return True
        if trimmed == FALSE_LITERAL:
            return False
        return None

    if is_numeric_literal(trimmed):
        return float(trimmed) if any(c in trimmed for c in ('.', 'e', 'E')) else int(trimmed)

    return trimmed


def is_boolean_or_null_literal(token: str) -> bool:
    return token in (TRUE_LITERAL, FALSE_LITERAL, NULL_LITERAL)


def is_numeric_literal(token: str) -> bool:
    if not token:
        return False
    if len(token) > 1 and token[0] == '0' and token[1] != '.':
        return False
    try:
        num = float(token)
    except ValueError:
        return False
    return num == num  # not NaN


def parse_string_literal(token: str) -> str:
    """Parse a quoted string literal."""
    trimmed = token.strip()
    if not trimmed.startswith(DOUBLE_QUOTE):
        return trimmed

    i = 1
    content: List[str] = []

    while i < len(trimmed):
        char = trimmed[i]
        if char == BACKSLASH and i + 1 < len(trimmed):
            content.append(char)
            content.append(trimmed[i + 1])
            i += 2
            continue
        if char == DOUBLE_QUOTE:
            if i != len(trimmed) - 1:
                raise ValueError('Unexpected characters after closing quote')
            return unescape_string(''.join(content))
        content.append(char)
        i += 1

    raise ValueError('Unterminated string: missing closing quote')


def unescape_string(value: str) -> str:
    """Unescape TOON escape sequences."""
    result = ''
    i = 0
    while i < len(value):
        char = value[i]
        if char == BACKSLASH:
            if i + 1 >= len(value):
                raise ValueError('Invalid escape sequence at end of string')
            nxt = value[i + 1]
            if nxt == 'n':
                result += NEWLINE
            elif nxt == 't':
                result += TAB
            elif nxt == 'r':
                result += CARRIAGE_RETURN
            elif nxt == BACKSLASH:
                result += BACKSLASH
            elif nxt == DOUBLE_QUOTE:
                result += DOUBLE_QUOTE
            else:
                raise ValueError(f'Invalid escape sequence: \\{nxt}')
            i += 2
        else:
            result += char
            i += 1
    return result


def parse_key_token(content: str, start: int = 0) -> Tuple[str, int]:
    """
    Parse a key token starting at ``start`` and return the key plus the index of
    the first character following the colon.
    """
    if start >= len(content):
        raise ValueError('Missing key')

    if content[start] == DOUBLE_QUOTE:
        return parse_quoted_key(content, start)
    return parse_unquoted_key(content, start)


def parse_unquoted_key(content: str, start: int) -> Tuple[str, int]:
    end = start
    while end < len(content) and content[end] != COLON:
        end += 1
    if end >= len(content) or content[end] != COLON:
        raise ValueError('Missing colon after key')
    key = content[start:end].strip()
    return key, end + 1


def parse_quoted_key(content: str, start: int) -> Tuple[str, int]:
    i = start + 1
    key_content = ''
    while i < len(content):
        char = content[i]
        if char == BACKSLASH and i + 1 < len(content):
            key_content += content[i : i + 2]
            i += 2
            continue
        if char == DOUBLE_QUOTE:
            if i + 1 >= len(content) or content[i + 1] != COLON:
                raise ValueError('Missing colon after key')
            parsed = unescape_string(key_content)
            return parsed, i + 2
        key_content += char
        i += 1
    raise ValueError('Unterminated quoted key')


def is_array_header_after_hyphen(content: str) -> bool:
    stripped = content.strip()
    return stripped.startswith(OPEN_BRACKET) and COLON in stripped


def is_object_first_field_after_hyphen(content: str) -> bool:
    return COLON in content
