"""
Constants mirroring the original TypeScript implementation.

These values are used across the encoder, decoder, and parser modules to keep
behaviour aligned with the canonical TOON implementation.
"""

from typing import Dict, Literal

# List item markers
LIST_ITEM_MARKER = '-'
LIST_ITEM_PREFIX = '- '

# Structural characters
COMMA = ','
COLON = ':'
SPACE = ' '
PIPE = '|'
HASH = '#'

# Brackets and braces
OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
OPEN_BRACE = '{'
CLOSE_BRACE = '}'

# Literal tokens
NULL_LITERAL = 'null'
TRUE_LITERAL = 'true'
FALSE_LITERAL = 'false'

# Escape characters
BACKSLASH = '\\'
DOUBLE_QUOTE = '"'
NEWLINE = '\n'
CARRIAGE_RETURN = '\r'
TAB = '\t'

# Delimiters
Delimiter = Literal[',', '\t', '|']
DelimiterKey = Literal['comma', 'tab', 'pipe']

DELIMITERS: Dict[DelimiterKey, Delimiter] = {
    'comma': COMMA,
    'tab': TAB,
    'pipe': PIPE,
}

DEFAULT_DELIMITER: Delimiter = DELIMITERS['comma']

# String escape sequences used when quoting
ESCAPE_SEQUENCES = {
    BACKSLASH: BACKSLASH + BACKSLASH,
    DOUBLE_QUOTE: BACKSLASH + DOUBLE_QUOTE,
    NEWLINE: BACKSLASH + 'n',
    CARRIAGE_RETURN: BACKSLASH + 'r',
}

# Backwards compatibility aliases for older imports in the codebase
QUOTE = DOUBLE_QUOTE
