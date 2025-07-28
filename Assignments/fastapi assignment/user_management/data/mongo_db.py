import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["user_management"]
collection = db["user_info"]
