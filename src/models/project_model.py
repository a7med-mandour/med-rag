from .basedatamodel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schema.project import Project



class ProjectModel(BaseDataModel):
    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.PROJECT_COLLECTION_NAME.value]

    async def create_project(self, project:Project):

        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id

        return project
    

    async def get_project_or_create_one(self, project_id:str):

        result = await self.collection.find_one({
            "project_id" : project_id
        })

        if not result :
            project = Project(project_id=project_id)
            project = await self.create_project(project)

            return project
        
        return Project(**result)

    async def get_all_projects(self, page:int=1, page_size:int=10):
       
        no_projects =await self.collection.count_documents({})

        no_pages= no_projects//page_size
        if no_projects%page_size >0:
            no_pages +=1

        cursor = await self.collection.find().skip((page-1) * page_size).limit(page_size)

        projects=[]
        async for project in cursor:
           projects.append(
               Project(**project)
           ) 

        return projects, no_pages

