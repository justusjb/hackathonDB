from pymongo import MongoClient
from settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

# Create MongoDB client at module level
mongo_client = MongoClient(settings.MONGODB_URI)

def get_db():
    return mongo_client[settings.mongodb_database]
