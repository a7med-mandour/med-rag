from .BaseController import BaseController
from models import ResponseEnums
import os


class ProjectController(BaseController):
    
    def __init__(self):
        super().__init__()
        
        
    def create_project_dir(self, project_id:str):
        
        project_dir = os.path.join(self.projects_dir, project_id)
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
            
        return project_dir
            
            
    