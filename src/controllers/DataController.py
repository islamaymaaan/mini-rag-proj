from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os



class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return (
                False, ResponseSignal.FILE_SIZE_EXCEEDED.value,
            )

        return True, ResponseSignal.FILE_UPLOAD_SUCESS.value

    def generate_unique_filepath(self, orig_filename: str, project_id: str):
        # Generate a unique filename using a timestamp or UUID
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
        
        return new_file_path , f"{random_key}_{cleaned_filename}"



    def get_cleaned_filename(self, orig_filename: str):
        # Remove special characters and spaces from the filename
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_filename.strip())
        cleaned_file_name = cleaned_file_name.replace(" ", "_")
        return cleaned_file_name
        