from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from models import ProcessingEnums
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



class ProcessController(BaseController):
    def __init__(self, project_id:str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().create_project_dir(project_id)
        
    def get_file_ext(self, file_id:str):
        
        return os.path.splitext(file_id)[-1]
    
   
    def get_data_loader(self, file_id:str):
        
        file_path = os.path.join(self.project_path,file_id)
        
        file_ext = self.get_file_ext(file_id=file_id) 
        
        if file_ext == ProcessingEnums.TXT.value:
            loader = TextLoader(file_path, encoding = 'utf-8')
        elif file_ext == ProcessingEnums.PDF.value:
            loader = PyMuPDFLoader(file_path)
        else:
            loader = None
            
        return loader
        
        
    def get_data_content(self,file_id:str):
        
        loader = self.get_data_loader(file_id=file_id)
        return loader.load()
    
    def process_data(self, data_content:list, 
                     file_id: str,
                     chunk_size:int = 100,
                     overlap:int = 20,
                     ):
        
        splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=chunk_size,
                                    chunk_overlap=overlap,
                                    length_function=len,
                                )
        
        data_content_text = [
            
            rec.page_content
            for rec in data_content
        ]
        
        data_content_meta =[
            
            rec.metadata
            for rec in data_content
        ]
        chunks = splitter.create_documents(
            data_content_text,
            metadatas = data_content_meta
        )
        
        return chunks