from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseEnums
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
        self.size_scale = 1048576 
        
    def validate_data(self, file:UploadFile):
        
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            return False, ResponseEnums.NOT_ALLOWED_FILE_TYPE.value
        
        if file.size > self.app_settings.ALLOWED_FILE_SIZE * self.size_scale :
            return False, ResponseEnums.SIZE_EXCEEDED.value
        
        return True, ResponseEnums.VALIDATION_SUCESS.value
        
        
    def get_unique_file_path(self, filename:str, project_path):
        
        # project_path = ProjectController().create_project_dir(project_id)
        random_key = self.create_random_key()
        cleaned_file_name = self.clean_file_name(filename=filename)
        
        random_name = os.path.join(
            project_path,
            random_key +'_'+cleaned_file_name
        )
        
        while os.path.exists(random_name):
            random_key = self.create_random_key()
            random_name = os.path.join(
                                project_path,
                                random_key +'_'+cleaned_file_name
                                       )
        return random_name
            
        
        
    def clean_file_name(self, filename:str):
        
        cleaned_file_name = re.sub(r'[^\w.]', '', filename.strip())

        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
    
            
            