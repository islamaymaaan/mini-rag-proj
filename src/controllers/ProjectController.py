from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os

class ProjectController(BaseController):
    """Manage the local directory used to store each project's RAG sources."""

    def __init__(self):
        """Initialize inherited settings and the shared assets directory.

        Returns:
            None: Project directories are created only when requested.
        """
        super().__init__()

    def get_project_path(self, project_id: str) :
        """Return a project's asset directory, creating it if needed.

        Args:
            project_id (str): Identifier of the project that owns the files.

        Returns:
            str: Local directory path where files await RAG processing.
        """

        project_path = os.path.join(self.file_dir, project_id)

        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return project_path
