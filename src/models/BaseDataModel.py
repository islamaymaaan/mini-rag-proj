from helpers.config import get_settings, Settings

class BaseDataModel:
    """Provide MongoDB access and application settings to data model classes.

    Concrete models use this shared setup to persist RAG projects, uploaded
    assets, and the chunks created from those assets.
    """

    def __init__(self, db_client : object):
        """Store the asynchronous MongoDB client used by a model.

        Args:
            db_client (object): Database handle supplied by the FastAPI app.

        Returns:
            None: Subclasses use the stored client to select their collection.
        """
        self.db_client = db_client
        self.app_settings = get_settings()
