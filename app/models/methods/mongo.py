from app import settings
from pymongo import MongoClient

class Methods_Mongo:
    @classmethod
    def get_db():
        client = MongoClient(settings.DATABASE_MONGO)
        mongoDb = client[settings.DATABASE_NAME]
        return mongoDb

    def get_collection(collection):
        client = MongoClient(settings.DATABASE_MONGO)
        mongoDb = client[settings.DATABASE_NAME]
        return mongoDb[collection]
