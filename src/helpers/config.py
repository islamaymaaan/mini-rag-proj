from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Load application, storage, database, and RAG chunking configuration.

    Values are read from the project's ``.env`` file, allowing the ingestion
    pipeline to use different databases and file limits per environment.
    """
    APP_NAME: str
    APP_VERSION: str
    GROQ_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE : int
    MONGODB_URL: str
    MONGODB_DATABASE: str
    

    class Config:
        """Tell Pydantic where to read environment values from."""
        env_file = ".env"


def get_settings():
    """Create the settings object used by the API and RAG pipeline.

    Returns:
        Settings: Configuration containing upload rules, MongoDB details, and
        chunking defaults.
    """
    return Settings()
