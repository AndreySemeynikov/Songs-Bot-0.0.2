from dataclasses import dataclass


@dataclass
class Document:
    """
    The Document class represents a document with a short identifier, filename, and content.
    """
    id: str  # Short identifier (e.g., "1", "2", ...)
    filename: str  # Full file name
    content: str  # File content
