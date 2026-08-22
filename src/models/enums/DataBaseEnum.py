from enum import Enum

class DataBaseEnum(Enum):
    """Centralize MongoDB collection names used by RAG persistence models."""
    COLLECTION_PROJECT_NAME = "projects"
    COLLECTION_CHUNK_NAME = "chunks"
    COLLECTION_ASSET_NAME = "asset"
