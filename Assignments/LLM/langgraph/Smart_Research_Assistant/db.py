from pymongo import MongoClient
from config import MONGO_URL,DB_NAME,COLLECTION_NAME
import os

client=MongoClient(MONGO_URL)
db=client[DB_NAME]
collection=db[COLLECTION_NAME]

def init_db():
    collection.create_index("query")

def save_query(query:str):
    result=collection.insert_one({"query":query})
    return str(result.inserted_id)

def get_all_queries():
    docs=collection.find().sort("_id",-1)
    return [{"id":str(d["_id"]) ,"query":d["query"]} for d in docs]

def get_recent_query():
    doc=collection.find().sort("_id",-1).limit(1)
    doc=next(doc,None)
    if doc:
        return {"id":str(doc["_id"]),"query":doc["query"]}
    return None