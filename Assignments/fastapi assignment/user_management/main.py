from fastapi import FastAPI,HTTPException,status,Depends
from jose import jwt
from config import SECRET_KEY,ALGORITHM,EXPIRE_TIME,HASHING
from models import User,Login,ChangePassword
from mongo_db import collection
from datetime import datetime,timedelta
import re


#----------- FastAPI Instance -------------
app=FastAPI(title="MY API APPLICATION")

#----------- TO check API is working are not(Health Check) --------------
@app.get("/")
async def health():
    return {"message":"API IS WORKING GOOD"}


#------------ Routes --------------------------
@app.post("/register")
async def register(data:User):
    if collection.find_one({"username":data.username}):
        return {"message":"user already exists with this email/phone number"}
    if not re.search(r"[a-z0-9]+@[a-z]+\.[a-z]+", data.username) and not re.search(r"\b\d{10}\b",data.username):
        return {"message":"Username must be a 10-digit phone number or a valid Gmail address"}
    hashed_password=HASHING.hash(data.password)
    #collection.insert_one({"password":hashed_password})
    user= { 
        "username": data.username,
        "firstname":data.firstname,
        "lastname":data.lastname,
        "dob": data.dob,
        "doj":data.doj,
        "password": hashed_password,
        "password_updated_at":datetime.utcnow(),
        "address":data.address,
        "comment":data.comment,
        "attempts":0,
        "status":data.status
       }
    collection.insert_one(user)
    return {"message":f"{data.firstname+data.lastname} registered successfully"}

@app.post("/login")
async def log_in(data:Login):
    user=collection.find_one({"username":data.username})
    #print(user)
    if not user:
        return {"message":"registration not found.please register"}
    if not HASHING.verify(data.password,user["password"]):
        return {"message":"password is incorrect"}
    if ((datetime.utcnow()- user["password_updated_at"])>timedelta(days=30)):
        return {"message":"password time is expired please change your password"}
    payload={"username":data.username,"exp":(datetime.utcnow()+timedelta(minutes=EXPIRE_TIME))}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    #user.update({"$set":{"status":"Active"}})
    collection.update_one(
    {"_id": user["_id"]},
    {"$set": {"status": "Active"}}
    )
    return {"message":"User logged in successfully","token":token,"token_type":"bearer"}

# @app.post("/change_password")
# async def change_password(data:ChangePassword,token:str=Depends(log_in)):

    
    
