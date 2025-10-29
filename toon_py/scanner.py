"""
Line scanner for TOON parsing.

This module provides utilities for parsing TOON text into lines with depth information.
"""

from typing import List

from .types import ParsedLine


def to_parsed_lines(input_text: str, indent_size: int = 2) -> List[ParsedLine]:
    """
    Parse TOON text into lines with depth information.
    
    Args:
        input_text: The TOON text to parse
        indent_size: Expected number of spaces per indentation level
        
    Returns:
        List of parsed lines with depth and content
    """
    lines = []
    
    for raw_line in input_text.split('\n'):
        # Skip empty lines
        if not raw_line.strip():
            continue
        
        # Count leading spaces
        indent = len(raw_line) - len(raw_line.lstrip())
        
        # Calculate depth (floor division)
        depth = indent // indent_size
        
        # Get content (without leading spaces)
        content = raw_line.lstrip()
        
        lines.append(ParsedLine(raw_line, depth, indent, content))
    
    return lines


class LineCursor:
    """
    Cursor for iterating over parsed lines.
    
    Provides peek and advance functionality for sequential line processing.
    """
    
    def __init__(self, lines: List[ParsedLine]):
        """
        Initialize the cursor.
        
        Args:
            lines: List of parsed lines
        """
        self.lines = lines
        self.index = 0
    
    def peek(self) -> ParsedLine:
        """
        Look at the current line without advancing.
        
        Returns:
            The current line, or None if at end
        """
        if self.index >= len(self.lines):
            return None
        return self.lines[self.index]
    
    def advance(self) -> ParsedLine:
        """
        Advance to the next line and return it.
        
        Returns:
            The next line, or None if at end
        """
        if self.index >= len(self.lines):
            return None
        line = self.lines[self.index]
        self.index += 1
        return line
    
    def at_end(self) -> bool:
        """
        Check if we've reached the end.
        
        Returns:
            True if at end, False otherwise
        """
        return self.index >= len(self.lines)
    
    @property
    def length(self) -> int:
        """Get the total number of lines."""
        return len(self.lines)
