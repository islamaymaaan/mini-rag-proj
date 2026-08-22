from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os



class DataController(BaseController):
    """Validate uploads and prepare safe, unique paths for RAG source files."""

    def __init__(self):
        """Set the byte conversion used when checking configured file sizes.

        Returns:
            None: Configuration and storage paths are inherited from
            ``BaseController``.
        """
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        """Check whether an uploaded file may enter the RAG ingestion pipeline.

        Args:
            file (UploadFile): FastAPI upload object containing the source file.

        Returns:
            tuple[bool, str]: Whether the file is accepted and a response signal
            explaining the validation result.
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return (
                False, ResponseSignal.FILE_SIZE_EXCEEDED.value,
            )

        return True, ResponseSignal.FILE_UPLOAD_SUCESS.value

    def generate_unique_filepath(self, orig_filename: str, project_id: str):
        """Build an unused disk path for a project's uploaded source file.

        Args:
            orig_filename (str): The name supplied by the uploading user.
            project_id (str): Project that owns the source file.

        Returns:
            tuple[str, str]: The absolute save path and the generated filename.
            This filename is later stored as the asset name used during chunking.
        """
        # Prefixing the cleaned name prevents two uploads from overwriting one another.
        random_key = self.generate_random_string() 
        project_path = ProjectController().get_project_path(project_id=project_id) 

        cleaned_filename = self.get_cleaned_filename(
            orig_filename=orig_filename
                                                     )
       
        new_file_path = os.path.join(
            project_path, f"{random_key}_{cleaned_filename}" 
            )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path, f"{random_key}_{cleaned_filename}"
            )
        
        return new_file_path, f"{random_key}_{cleaned_filename}"

    def get_cleaned_filename(self, orig_filename: str):
        """Remove unsafe characters from an uploaded filename.

        Args:
            orig_filename (str): Original user-provided filename.

        Returns:
            str: A filename containing only word characters and periods, suitable
            for local RAG asset storage.
        """
        # Keep the extension so the processor can select the right document loader.
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_filename.strip())
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        return cleaned_file_name
