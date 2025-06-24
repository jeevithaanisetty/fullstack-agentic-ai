import pymongo  #only upto python-3.12(fullstack-agentic-ai env 3.12)
from pymongo import MongoClient

client=pymongo.MongoClient("localhost",27017)
db=client["College"]
collection=db["students"]
info=[
    {"name":"ram","roll_no":"E123"},
    {"name":"uday","roll_no":"S143"},
    {"name":"sai","roll_no":"T678"}
]
Collection=collection.insert_many(info)
print(Collection.inserted_ids)
for x in collection.find():
    print(x)

