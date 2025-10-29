"""
Encoding helpers that mirror the TypeScript implementation.

The functions in this module are intentionally close to the original source so
that behavioural parity is maintained between the Python port and the reference
library.
"""

from typing import Iterable, Optional

from .constants import LIST_ITEM_MARKER, LIST_ITEM_PREFIX
from .normalize import (
    is_array_of_arrays,
    is_array_of_objects,
    is_array_of_primitives,
    is_json_array,
    is_json_object,
    is_json_primitive,
)
from .primitives import (
    encode_and_join_primitives,
    encode_key,
    encode_primitive,
    format_header,
)
from .types import Depth, JsonArray, JsonObject, JsonPrimitive, JsonValue, ResolvedEncodeOptions
from .writer import LineWriter


def encode_value(value: JsonValue, options: ResolvedEncodeOptions) -> str:
    """Encode a normalised JsonValue into TOON text."""
    if is_json_primitive(value):
        return encode_primitive(value, options.delimiter)

    writer = LineWriter(options.indent)

    if is_json_array(value):
        encode_array(None, value, writer, 0, options)
    elif is_json_object(value):
        encode_object(value, writer, 0, options)

    return writer.to_string()


def encode_object(value: JsonObject, writer: LineWriter, depth: Depth, options: ResolvedEncodeOptions) -> None:
    """Encode an object by walking its key/value pairs."""
    for key, member in value.items():
        encode_key_value_pair(key, member, writer, depth, options)


def encode_key_value_pair(key: str, value: JsonValue, writer: LineWriter, depth: Depth, options: ResolvedEncodeOptions) -> None:
    """Encode a single key/value pair."""
    encoded_key = encode_key(key)

    if is_json_primitive(value):
        writer.push(depth, f'{encoded_key}: {encode_primitive(value, options.delimiter)}')
    elif is_json_array(value):
        encode_array(key, value, writer, depth, options)
    elif is_json_object(value):
        nested_keys = list(value.keys())
        if not nested_keys:
            writer.push(depth, f'{encoded_key}:')
        else:
            writer.push(depth, f'{encoded_key}:')
            encode_object(value, writer, depth + 1, options)


def encode_array(
    key: Optional[str],
    value: JsonArray,
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Encode an array, selecting the appropriate representation."""
    if len(value) == 0:
        writer.push(
            depth,
            format_header(
                0,
                key=key,
                delimiter=options.delimiter,
                length_marker=options.lengthMarker,
            ),
        )
        return

    if is_array_of_primitives(value):
        encode_inline_primitive_array(key, value, writer, depth, options)
        return

    if is_array_of_arrays(value):
        if all(is_array_of_primitives(arr) for arr in value):
            encode_array_of_arrays_as_list_items(key, value, writer, depth, options)
            return

    if is_array_of_objects(value):
        header = extract_tabular_header(value)
        if header:
            encode_array_of_objects_as_tabular(key, value, header, writer, depth, options)
        else:
            encode_mixed_array_as_list_items(key, value, writer, depth, options)
        return

    encode_mixed_array_as_list_items(key, value, writer, depth, options)


def encode_inline_primitive_array(
    prefix: Optional[str],
    values: Iterable[JsonPrimitive],
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Encode a primitive array as a single inline row."""
    line = encode_inline_array_line(
        values,
        options.delimiter,
        prefix=prefix,
        length_marker=options.lengthMarker,
    )
    writer.push(depth, line)


def encode_array_of_arrays_as_list_items(
    prefix: Optional[str],
    values: JsonArray,
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Encode an array of primitive arrays using list-item notation."""
    header = format_header(
        len(values),
        key=prefix,
        delimiter=options.delimiter,
        length_marker=options.lengthMarker,
    )
    writer.push(depth, header)

    for arr in values:
        if is_array_of_primitives(arr):
            inline = encode_inline_array_line(
                arr,
                options.delimiter,
                length_marker=options.lengthMarker,
            )
            writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{inline}')


def encode_inline_array_line(
    values: Iterable[JsonPrimitive],
    delimiter: str,
    *,
    prefix: Optional[str] = None,
    length_marker: Optional[str | bool] = False,
) -> str:
    """Encode an inline array header plus optional value list."""
    values_list = list(values)
    header = format_header(
        len(values_list),
        key=prefix,
        delimiter=delimiter,
        length_marker=length_marker,
    )
    if not values_list:
        return header
    joined = encode_and_join_primitives(values_list, delimiter)
    separator = '\t' if delimiter == '\t' else ' '
    return f'{header}{separator}{joined}'


def encode_array_of_objects_as_tabular(
    prefix: Optional[str],
    rows: JsonArray,
    header: list[str],
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Encode a uniform array of objects using the tabular representation."""
    header_line = format_header(
        len(rows),
        key=prefix,
        fields=header,
        delimiter=options.delimiter,
        length_marker=options.lengthMarker,
    )
    writer.push(depth, header_line)
    write_tabular_rows(rows, header, writer, depth + 1, options)


def extract_tabular_header(rows: JsonArray) -> Optional[list[str]]:
    """Return a header list when an array qualifies for the tabular format."""
    if not rows:
        return None

    first_row = rows[0]
    if not isinstance(first_row, dict):
        return None

    header = list(first_row.keys())
    if not header:
        return None

    if is_tabular_array(rows, header):
        return header
    return None


def is_tabular_array(rows: JsonArray, header: list[str]) -> bool:
    """Check whether every object matches the first object's keys and primitive values."""
    for row in rows:
        if not isinstance(row, dict):
            return False
        keys = list(row.keys())
        if len(keys) != len(header):
            return False
        for key in header:
            if key not in row or not is_json_primitive(row[key]):
                return False
    return True


def write_tabular_rows(
    rows: JsonArray,
    header: list[str],
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Write each tabular row using the active delimiter."""
    for row in rows:
        if not isinstance(row, dict):
            continue
        values = [row[key] for key in header]
        joined = encode_and_join_primitives(values, options.delimiter)
        writer.push(depth, joined)


def encode_mixed_array_as_list_items(
    prefix: Optional[str],
    values: JsonArray,
    writer: LineWriter,
    depth: Depth,
    options: ResolvedEncodeOptions,
) -> None:
    """Encode arrays that fall back to list-item notation."""
    header = format_header(
        len(values),
        key=prefix,
        delimiter=options.delimiter,
        length_marker=options.lengthMarker,
    )
    writer.push(depth, header)

    for item in values:
        if is_json_primitive(item):
            writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{encode_primitive(item, options.delimiter)}')
        elif is_json_array(item):
            if is_array_of_primitives(item):
                inline = encode_inline_array_line(
                    item,
                    options.delimiter,
                    length_marker=options.lengthMarker,
                )
                writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{inline}')
            else:
                encode_array(None, item, writer, depth + 1, options)
        elif is_json_object(item):
            encode_object_as_list_item(item, writer, depth + 1, options)


def encode_object_as_list_item(obj: JsonObject, writer: LineWriter, depth: Depth, options: ResolvedEncodeOptions) -> None:
    """Encode an object that appears inside a list."""
    keys = list(obj.keys())
    if not keys:
        writer.push(depth, LIST_ITEM_MARKER)
        return

    first_key = keys[0]
    first_value = obj[first_key]
    encoded_first_key = encode_key(first_key)

    if is_json_primitive(first_value):
        writer.push(depth, f'{LIST_ITEM_PREFIX}{encoded_first_key}: {encode_primitive(first_value, options.delimiter)}')
    elif is_json_array(first_value):
        if is_array_of_primitives(first_value):
            inline = encode_inline_array_line(
                first_value,
                options.delimiter,
                prefix=first_key,
                length_marker=options.lengthMarker,
            )
            writer.push(depth, f'{LIST_ITEM_PREFIX}{inline}')
        elif is_array_of_objects(first_value):
            header = extract_tabular_header(first_value)
            if header:
                header_line = format_header(
                    len(first_value),
                    key=first_key,
                    fields=header,
                    delimiter=options.delimiter,
                    length_marker=options.lengthMarker,
                )
                writer.push(depth, f'{LIST_ITEM_PREFIX}{header_line}')
                write_tabular_rows(first_value, header, writer, depth + 1, options)
            else:
                writer.push(depth, f'{LIST_ITEM_PREFIX}{encoded_first_key}[{len(first_value)}]:')
                for nested in first_value:
                    if isinstance(nested, dict):
                        encode_object_as_list_item(nested, writer, depth + 1, options)
                    elif is_json_primitive(nested):
                        writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{encode_primitive(nested, options.delimiter)}')
                    elif is_json_array(nested) and is_array_of_primitives(nested):
                        inline = encode_inline_array_line(
                            nested,
                            options.delimiter,
                            length_marker=options.lengthMarker,
                        )
                        writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{inline}')
        else:
            writer.push(depth, f'{LIST_ITEM_PREFIX}{encoded_first_key}[{len(first_value)}]:')
            for nested in first_value:
                if is_json_primitive(nested):
                    writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{encode_primitive(nested, options.delimiter)}')
                elif is_json_array(nested) and is_array_of_primitives(nested):
                    inline = encode_inline_array_line(
                        nested,
                        options.delimiter,
                        length_marker=options.lengthMarker,
                    )
                    writer.push(depth + 1, f'{LIST_ITEM_PREFIX}{inline}')
                elif is_json_object(nested):
                    encode_object_as_list_item(nested, writer, depth + 1, options)
    elif is_json_object(first_value):
        nested_keys = list(first_value.keys())
        if not nested_keys:
            writer.push(depth, f'{LIST_ITEM_PREFIX}{encoded_first_key}:')
        else:
            writer.push(depth, f'{LIST_ITEM_PREFIX}{encoded_first_key}:')
            encode_object(first_value, writer, depth + 2, options)

    for extra_key in keys[1:]:
        encode_key_value_pair(extra_key, obj[extra_key], writer, depth + 1, options)
