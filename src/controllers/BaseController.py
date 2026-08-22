from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    """Provide shared settings and file-system utilities for RAG controllers.

    Controllers use this base class to find the local asset directory and to
    generate identifiers for uploaded source files before they are processed
    into RAG chunks.
    """

    def __init__(self):
        """Initialize shared configuration and the root directory for assets.

        Returns:
            None: The controller keeps the settings and asset path as instance
            attributes for subclasses such as ``DataController``.
        """
        self.app_settings = get_settings()

        # ``src`` is the application base; uploaded RAG sources live below it.
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets/files")

    def generate_random_string(self, length: int=12):
        """Create a short random identifier for a stored source file.

        Args:
            length (int): Number of letters and digits to generate. Defaults to
                12.

        Returns:
            str: A random alphanumeric string used to avoid filename collisions
            in the RAG pipeline's asset storage.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
