from .basedatamodel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schema.chunks import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne




class TextChunkModel(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client=db_client)
        self.collection = db_client[DataBaseEnum.TEXT_CHUNK_COLLECTION_NAME.value]


    async def create_chunk(self, chunk:DataChunk):
        data = await self.collection.insert_one(chunk.model_dump())
        chunk._id = data.inserted_id

        return chunk
    

    async def get_chunk(self, chunk_id):
        data = self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })
        if not data:
            return None

        return DataChunk(**data)


    async def insert_many_chunks(self, chunks:list, patch_size:int = 100):
        
        for i in range(0,len(chunks),patch_size):
            batch = chunks[i:patch_size+i]

        operations = [
            InsertOne(chunk.model_dump())
            for chunk in batch
        ]
        await self.collection.bulk_write(operations)

        return len(chunks)
    

    async def do_reset_by_project_id(self, project_id:ObjectId):

        result = await self.collection.delete_many({
            "chunk_project_id":project_id
        })
        return result.deleted_count