from fastapi import FastAPI,HTTPException,status,Depends,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from config import SECRET_KEY,ALGORITHM,EXPIRE_TIME,HASHING,MAX_ATTEMPTS
from models import User,Login,ChangePassword,Forgotted
from mongo_db import collection
from datetime import datetime,timedelta
import smtplib 
from email.message import EmailMessage

import re

token_black_list=[]

#----------- FastAPI Instance -------------
app=FastAPI(title="MY API APPLICATION")

#----------- TO check API is working are not(Health Check) --------------
@app.get("/")
async def health():
    return {"message":"API IS WORKING GOOD"}

oauth2_shceme=OAuth2PasswordBearer(tokenUrl="login")

#------------ Routes --------------------------
@app.post("/register")
async def register(data:User):
    if collection.find_one({"username":data.username}):
        return {"message":"user already exists with this email/phone number"}
    if not re.match(r"[a-z0-9]+@[a-z]+\.[a-z]+", data.username) and not re.match(r"\b\d{10}\b",data.username):
        return {"message":"Username must be a 10-digit phone number or a valid Gmail address"}
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",data.password):
        raise HTTPException(status_code=400,detail="Password must contain at least one capital letter, one small letter, one digit, one special character, and be at least 8 characters long")
    hashed_password=HASHING.hash(data.password)
    #collection.insert_one({"password":hashed_password})
    user= { 
        "username": data.username,
        "firstname":data.firstname,
        "lastname":data.lastname,
        "dob": data.dob,
        "doj":data.doj,
        "password": hashed_password,
        "password_updated_at":datetime.now(),
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

def get_current_user(token:str=Depends(oauth2_shceme)):
    try:
        if token in token_black_list:
            raise HTTPException(status_code=400, detail="token is blocked please login again to get token")
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username=payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

@app.post("/change_password")
async def change_password(data:ChangePassword,user:str=Depends(get_current_user)):
    #user=Depends(get_current_user) throwing err as TypeError: 'Depends' object is not subscriptable
    attempts = user.get("attempts", 0)
    if attempts == MAX_ATTEMPTS:
        raise HTTPException(status_code=403, detail="Maximum attempts reached. Try again after 24 hours.")
    if not HASHING.verify(data.password,user["password"]):
        collection.update_one(
        {"_id": user["_id"]}, {"$set": {"attempts": attempts + 1,"attempt_time":datetime.now()}}
        )
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    if attempts == MAX_ATTEMPTS:
        if datetime.now()-user.get("attempt_time")>=timedelta(hours=24):
             collection.update_one(
                {"_id": user["_id"]}, {"$set": {"attempts":0,"attempt_time":None}}
            )
    if user["status"] != "Active":
        raise HTTPException(status_code=403, detail="Please login to change password")
    if data.password==data.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from the old password")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",data.new_password):
        raise HTTPException(status_code=400,detail="Password must contain at least one capital letter, one small letter, one digit, one special character, and be at least 8 characters long")
    
    hashed_new_password = HASHING.hash(data.new_password)
    collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "password": hashed_new_password,
                "password_updated_at": datetime.now()
            }
        }
    )
    
    return {"message": "Password changed successfully"}

async def send_link(request:Request):
    link=request.url_for("change_password")
    return str(link)

@app.post("/forget_password")
async def forget_password(data:Forgotted,request:Request,user:str=Depends(get_current_user)):
    to_email=user.get("username")
    from_email="jeevithamolamanti@gmail.com"
    password="jfta vhtp ulcn dizo"
    body=await send_link(request)

    msg=EmailMessage()
    msg.set_content(body)
    msg["Subject"]=data.subject
    msg["From"]=from_email
    msg["To"]=to_email

    with smtplib.SMTP_SSL("smtp.gmail.com",465)as smtp:
        smtp.login(from_email,password)
        smtp.send_message(msg)
    return {"message":"Email sent successfully"}

@app.post("/logout")
async def log_out(token:str=Depends(oauth2_shceme),user:str=Depends(get_current_user)):
    username=user.get("username")
    payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    user_name=payload.get("username")
    if username!=user_name:
        raise HTTPException(status_code=400, detail="entered token is invalid or token expired")
    token_black_list.append(token)
    return {"message":"user_logged_out successfully"}


    
