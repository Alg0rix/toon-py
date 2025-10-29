"""
Line writer ensuring spacing matches the TypeScript reference.
"""

from .constants import LIST_ITEM_MARKER, LIST_ITEM_PREFIX


class LineWriter:
    """Accumulates lines with indentation that mimics the TS implementation."""
    
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size
        self.lines: list[str] = []
    
    def push(self, depth: int, content: str) -> None:
        content = content.rstrip()
        indent_depth = depth
        
        if depth > 0 and (content.startswith(LIST_ITEM_PREFIX) or content == LIST_ITEM_MARKER):
            indent_depth = max(0, depth - 1)
        
        indent = ' ' * (indent_depth * self.indent_size)
        self.lines.append(indent + content)
    
    def to_string(self) -> str:
        return '\n'.join(self.lines)
    
    def __str__(self) -> str:
        return self.to_string()
    
    def __repr__(self) -> str:
        return f"LineWriter(indent_size={self.indent_size}, lines={len(self.lines)})"
