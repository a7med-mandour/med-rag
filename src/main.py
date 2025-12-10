from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from routes import base, data
from helper.config import get_settings
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("opening the app and connecting to database")

    setting = get_settings()

    app.mongo_collection = AsyncIOMotorClient(setting.MONGO_URL)

    app.db_client = app.mongo_collection[setting.MONGO_DATABASE]

    print("Connected to MongoDB!")

    yield

    print("app closure")
    app.mongo_collection.close()


    

app = FastAPI(lifespan=lifespan)



app.include_router(base.base_router)
app.include_router(data.data_router)