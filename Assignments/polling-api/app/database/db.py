from app.core.config import MONGO_URL
import pymongo

client=pymongo.MongoClient(MONGO_URL)
db=client.DATABASE_NAME