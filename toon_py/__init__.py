"""
Python implementation of TOON (Token-Oriented Object Notation)
A token-efficient JSON alternative for LLM prompts, following the original @byjohann/toon specification.

This implementation adheres to the TOON v1.1 specification and is compatible with the
original TypeScript/JavaScript implementation.

Example usage:
    >>> from toon_py import encode, decode
    >>> 
    >>> data = {"name": "Ada", "age": 30, "tags": ["admin", "dev"]}
    >>> toon_str = encode(data)
    >>> print(toon_str)
    name: Ada
    age: 30
    tags[2]: admin,dev
    >>> 
    >>> decoded = decode(toon_str)
    >>> print(decoded)
    {'name': 'Ada', 'age': 30, 'tags': ['admin', 'dev']}
"""

from .encoder import encode
from .decoder import decode
from .constants import DEFAULT_DELIMITER, DELIMITERS

__version__ = "0.1.0"
__author__ = "TOON Python Contributors"
__license__ = "MIT"
__all__ = ["encode", "decode", "DEFAULT_DELIMITER", "DELIMITERS"]
