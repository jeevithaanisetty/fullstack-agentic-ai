from core.config import MONGO_URL,DATABASE_NAME
import pymongo

client=pymongo.Mongoclient(MONGO_URL)
db=client(DATABASE_NAME)