from enum import Enum

class ProcessingEnum(str, Enum):
    """List file extensions that have document loaders in the RAG pipeline."""
    TXT = ".txt"
    PDF = ".pdf"
