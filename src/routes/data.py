from fastapi import FastAPI, APIRouter , Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from controllers import DataController, ProjectController, ProcessController
from models.project_model import ProjectModel
from models.TextChunkModel import TextChunkModel
from models.db_schema.chunks import DataChunk

import os
import aiofiles
from models import ResponseEnums
from .schemas import DataSchema




data_router = APIRouter(
    prefix='/api/v1/data'
)

@data_router.post('/upload/{project_id}')
async def data_upload(request:Request,project_id:str , file:UploadFile
                      ):
    
    project_model = ProjectModel(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    
    data_controller = DataController()
    validate, message = data_controller.validate_data(file=file)
    
    if not validate:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": message
            }
        )
        
    project_path = ProjectController().create_project_dir(project_id=project_id)
    # file_path = os.path.join(project_path, file.filename)
    file_path,file_id = data_controller.get_unique_file_path(file.filename, project_path=project_path)
    
    try:
        
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(data_controller.app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        print(e)
        
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseEnums.FILE_UPLOADE_FAILED.value
            }
        )   
    
    return JSONResponse(
          
            content={
                "signal": ResponseEnums.FILE_UPLOADED_SUCCESSFULLY.value,
                "file_id": file_id,
                "pro": str(project.id)
                
            }
        )
        
    
@data_router.post('/process/{project_id}')
async def data_processing(request:Request,project_id:str, process_request:DataSchema):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap = process_request.overlap

    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)


    process_controller = ProcessController(project_id=project_id)
    
    data_content = process_controller.get_data_content(file_id=file_id)
    
    chunks = process_controller.process_data(
        data_content,
        file_id,
        chunk_size,
        overlap=overlap
    )
    
    if chunks is None or len(chunks) == 0 :
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseEnums.NO_CHUNK_FOUND.value
            }
        )
    
    data_chunks = [
         DataChunk(
             chunk_text = chunk.page_content,
             metadata= chunk.metadata,
             chunk_order= i+1,
             chunk_project_id = project.id
             
         )
         for i, chunk in enumerate(chunks)
         ]
        

    chunk_model = TextChunkModel(db_client=request.app.db_client)

    no_chunks = await chunk_model.insert_many_chunks(data_chunks)

    return no_chunks