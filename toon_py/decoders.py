"""
Decoding helpers aligned with the TypeScript implementation.

The code here is a direct translation of the canonical TOON decoder so that the
Python port matches the behaviour of the original library.
"""

from __future__ import annotations

from typing import Optional, Tuple

from .constants import COLON, DEFAULT_DELIMITER, LIST_ITEM_MARKER, LIST_ITEM_PREFIX
from .parser import (
    is_array_header_after_hyphen,
    is_object_first_field_after_hyphen,
    map_row_values_to_primitives,
    parse_array_header_line,
    parse_delimited_values,
    parse_key_token,
    parse_primitive_token,
)
from .scanner import LineCursor
from .types import ArrayHeaderInfo, Depth, JsonArray, JsonObject, JsonPrimitive, JsonValue, ParsedLine, ResolvedDecodeOptions


def decode_value_from_lines(cursor: LineCursor, options: ResolvedDecodeOptions) -> JsonValue:
    """Decode a value starting at the cursor."""
    first = cursor.peek()
    if not first:
        raise ValueError('No content to decode')

    if is_root_array_header_line(first):
        header_info = parse_array_header_line(first.content, DEFAULT_DELIMITER)
        if header_info:
            cursor.advance()
            return decode_array_from_header(header_info['header'], header_info.get('inlineValues'), cursor, 0, options)

    if cursor.length == 1 and not is_key_value_line(first):
        return parse_primitive_token(first.content.strip())

    return decode_object(cursor, 0, options)


def is_root_array_header_line(line: ParsedLine) -> bool:
    return is_array_header_after_hyphen(line.content)


def is_key_value_line(line: ParsedLine) -> bool:
    content = line.content
    if content.startswith('"'):
        i = 1
        while i < len(content):
            if content[i] == '\\' and i + 1 < len(content):
                i += 2
                continue
            if content[i] == '"':
                return i + 1 < len(content) and content[i + 1] == COLON
            i += 1
        return False
    return COLON in content


def decode_object(cursor: LineCursor, base_depth: Depth, options: ResolvedDecodeOptions) -> JsonObject:
    obj: JsonObject = {}

    while not cursor.at_end():
        line = cursor.peek()
        if not line or line.depth < base_depth:
            break

        if line.depth == base_depth:
            key, value = decode_key_value_pair(line, cursor, base_depth, options)
            obj[key] = value
        else:
            break

    return obj


def decode_key_value_pair(
    line: ParsedLine,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> Tuple[str, JsonValue]:
    cursor.advance()
    key, value, _ = decode_key_value(line.content, cursor, base_depth, options)
    return key, value


def decode_key_value(
    content: str,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> Tuple[str, JsonValue, Depth]:
    array_header = parse_array_header_line(content, DEFAULT_DELIMITER)
    if array_header and array_header['header'].key:
        value = decode_array_from_header(array_header['header'], array_header.get('inlineValues'), cursor, base_depth, options)
        return array_header['header'].key, value, base_depth + 1

    key, end = parse_key_token(content, 0)
    rest = content[end:].strip()

    if not rest:
        next_line = cursor.peek()
        if next_line and next_line.depth > base_depth:
            nested = decode_object(cursor, base_depth + 1, options)
            return key, nested, base_depth + 1
        return key, {}, base_depth + 1

    value = parse_primitive_token(rest)
    return key, value, base_depth + 1


def decode_array_from_header(
    header: ArrayHeaderInfo,
    inline_values: Optional[str],
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> JsonArray:
    if inline_values is not None and inline_values.strip():
        return decode_inline_primitive_array(header, inline_values, options)

    if header.fields:
        return decode_tabular_array(header, cursor, base_depth, options)

    return decode_list_array(header, cursor, base_depth, options)


def _coalesce_inline_values(values: list[str], expected: int, delimiter: str) -> list[str]:
    """Merge tokens when delimited parsing produced more segments than expected."""
    if expected <= 0:
        return values
    if len(values) == expected:
        return values
    if len(values) < expected:
        return values

    if len(values) % expected == 0:
        chunk_size = len(values) // expected
        if chunk_size > 1:
            return [
                delimiter.join(values[i : i + chunk_size])
                for i in range(0, len(values), chunk_size)
            ]

    if expected > 1 and len(values) > expected:
        head = values[: expected - 1]
        tail = delimiter.join(values[expected - 1 :])
        return head + [tail]

    return values


def decode_inline_primitive_array(
    header: ArrayHeaderInfo,
    inline_values: str,
    options: ResolvedDecodeOptions,
) -> JsonArray:
    values = parse_delimited_values(inline_values, header.delimiter)
    values = _coalesce_inline_values(values, header.length, header.delimiter)
    primitives = map_row_values_to_primitives(values)
    assert_expected_count(len(primitives), header.length, 'inline array items', options)
    return primitives


def decode_list_array(
    header: ArrayHeaderInfo,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> JsonArray:
    items: JsonArray = []
    item_depth = base_depth + 1

    candidate_depths = {item_depth}
    if item_depth > 0:
        candidate_depths.add(item_depth - 1)

    min_depth = min(candidate_depths)

    while not cursor.at_end() and len(items) < header.length:
        line = cursor.peek()
        if not line or line.depth < min_depth:
            break

        if line.depth in candidate_depths:
            if line.content == LIST_ITEM_MARKER:
                cursor.advance()
                items.append({})
                continue
            if line.content.startswith(LIST_ITEM_PREFIX):
                item = decode_list_item(cursor, item_depth, header.delimiter, options)
                items.append(item)
                continue

            nested_header = parse_array_header_line(line.content, header.delimiter)
            if nested_header:
                cursor.advance()
                nested = decode_array_from_header(
                    nested_header['header'],
                    nested_header.get('inlineValues'),
                    cursor,
                    item_depth,
                    options,
                )
                items.append(nested)
                continue

        break

    assert_expected_count(len(items), header.length, 'list array items', options)

    if options.strict and not cursor.at_end():
        next_line = cursor.peek()
        if next_line and next_line.depth in candidate_depths:
            if next_line.content.startswith(LIST_ITEM_PREFIX):
                raise ValueError(f'Expected {header.length} list array items, but found more')
            if next_line.content == LIST_ITEM_MARKER:
                raise ValueError(f'Expected {header.length} list array items, but found more')

    return items


def decode_tabular_array(
    header: ArrayHeaderInfo,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> JsonArray:
    objects: JsonArray = []
    row_depth = base_depth + 1

    while not cursor.at_end() and len(objects) < header.length:
        line = cursor.peek()
        if not line or line.depth < row_depth:
            break

        if line.depth == row_depth:
            cursor.advance()
            values = parse_delimited_values(line.content, header.delimiter)
            values = _coalesce_row_values(values, len(header.fields or []), header.delimiter)
            assert_expected_count(len(values), len(header.fields or []), 'tabular row values', options)

            primitives = map_row_values_to_primitives(values)
            obj: JsonObject = {}

            for idx, field in enumerate(header.fields or []):
                obj[field] = primitives[idx]

            objects.append(obj)
        else:
            break

    assert_expected_count(len(objects), header.length, 'tabular rows', options)

    if options.strict and not cursor.at_end():
        next_line = cursor.peek()
        if next_line and next_line.depth == row_depth and not next_line.content.startswith(LIST_ITEM_PREFIX):
            has_colon = COLON in next_line.content
            has_delimiter = header.delimiter in next_line.content
            if not has_colon:
                raise ValueError(f'Expected {header.length} tabular rows, but found more')
            if has_delimiter:
                colon_pos = next_line.content.index(COLON)
                delimiter_pos = next_line.content.index(header.delimiter)
                if delimiter_pos < colon_pos:
                    raise ValueError(f'Expected {header.length} tabular rows, but found more')

    return objects


def _coalesce_row_values(values: list[str], expected: int, delimiter: str) -> list[str]:
    if expected <= 0:
        return values
    if len(values) == expected:
        return values
    if len(values) > expected:
        head = values[: expected - 1]
        tail = delimiter.join(values[expected - 1 :])
        return head + [tail]
    return values


def decode_list_item(
    cursor: LineCursor,
    base_depth: Depth,
    active_delimiter: str,
    options: ResolvedDecodeOptions,
) -> JsonValue:
    line = cursor.advance()
    if not line:
        raise ValueError('Expected list item')

    if line.content == LIST_ITEM_MARKER:
        return {}

    after_hyphen = line.content[len(LIST_ITEM_PREFIX) :]

    if not after_hyphen.strip():
        return {}

    if is_array_header_after_hyphen(after_hyphen):
        array_header = parse_array_header_line(after_hyphen, active_delimiter)
        if array_header:
            return decode_array_from_header(array_header['header'], array_header.get('inlineValues'), cursor, base_depth, options)

    if is_object_first_field_after_hyphen(after_hyphen):
        return decode_object_from_list_item(line, cursor, base_depth, options)

    return parse_primitive_token(after_hyphen)


def decode_object_from_list_item(
    first_line: ParsedLine,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> JsonObject:
    after_hyphen = first_line.content[len(LIST_ITEM_PREFIX) :]
    key, value, follow_depth = decode_first_field_on_hyphen(after_hyphen, cursor, base_depth, options)

    obj: JsonObject = {key: value}

    while not cursor.at_end():
        line = cursor.peek()
        if not line or line.depth < follow_depth:
            break

        if line.depth == follow_depth and not line.content.startswith(LIST_ITEM_PREFIX):
            k, v = decode_key_value_pair(line, cursor, follow_depth, options)
            obj[k] = v
        else:
            break

    return obj


def decode_first_field_on_hyphen(
    rest: str,
    cursor: LineCursor,
    base_depth: Depth,
    options: ResolvedDecodeOptions,
) -> Tuple[str, JsonValue, Depth]:
    return decode_key_value(rest, cursor, base_depth, options)


def assert_expected_count(actual: int, expected: int, label: str, options: ResolvedDecodeOptions) -> None:
    if options.strict and actual != expected:
        raise ValueError(f'Expected {expected} {label}, but got {actual}')
