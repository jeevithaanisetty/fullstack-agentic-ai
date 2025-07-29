from fastapi import FastAPI,HTTPException,status,Depends,Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from config.config import SECRET_KEY,ALGORITHM,EXPIRE_TIME,HASHING,MAX_ATTEMPTS
from model.models import User,Login,ChangePassword,Forgotted,Reset
from data.mongo_db import collection
from datetime import datetime,timedelta
import smtplib 
from email.message import EmailMessage
from utils.logger import get_logger
from utils.decorator import handle_exceptions
import os
import re
import random

logger=get_logger("users.main")
token_black_list=[]

#------ env variables -------
mail=os.environ.get("MY_MAIL")
app_password=os.environ.get("APP_PASSWORD")

#----------- FastAPI Instance -------------
app=FastAPI(title="MY API APPLICATION")

#----------- API Health Check --------------
@app.get("/")
async def health():
    return {"message":"API IS WORKING GOOD"}

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

#------------ Routes --------------------------

@handle_exceptions
@app.post("/register")
async def register(data:User):
    if collection.find_one({"username":data.username}):
        logger.info("user already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists with this email/phone number")
    if not re.match(r"[a-z0-9]+@[a-z]+\.[a-z]+", data.username) and not re.match(r"\b\d{10}\b",data.username):    # r"^[\w\.-]+@[\w\.-]+\.\w+$"
        logger.info("ivalid email/phone no")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username must be a 10-digit phone number or a valid Gmail address")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",data.password):
        logger.info("invalid password")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password must contain at least one capital letter, one small letter, one digit, one special character, and be at least 8 characters long")
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
    logger.info("user registered")
    return {"message":f"{data.firstname+data.lastname} registered successfully"}

@handle_exceptions
@app.post("/login")
async def log_in(data:Login):
    user=collection.find_one({"username":data.username})
    #print(user)
    if not user:
        logger.info("user not registered")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Registration not found. Please register.")
    if not HASHING.verify(data.password,user["password"]):
        logger.error("imcorrect password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password is incorrect")
    if ((datetime.now()- user["password_updated_at"])>timedelta(days=30)):
        logger.info("password reached max time limit")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You changed your password 30 days ago. Please change it again.")
    payload={"username":data.username,"exp":(datetime.utcnow()+timedelta(minutes=EXPIRE_TIME))}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    #user.update({"$set":{"status":"Active"}})
    collection.update_one(
    {"_id": user["_id"]},
    {"$set": {"status": "Active"}}
    )
    logger.info("user login successful and token generated")
    return {"message":"User logged in successfully","token":token,"token_type":"bearer"}

@handle_exceptions
def get_current_user(token:str=Depends(oauth2_scheme)):
    try:
        if token in token_black_list:
            logger.info("token is blacklisted")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Token is blocked. Please login again to get a new token.")
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username=payload.get("username")
        if not username:
            logger.info("token is invalid")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token payload")
        user = collection.find_one({"username": username})
        if not user:
            logger.info("user not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except JWTError as e:
        logger.error("token is invalid or expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is invalid or expired")
    
@handle_exceptions
@app.post("/change_password")
async def change_password(data:ChangePassword,user:dict=Depends(get_current_user)):
    #user=Depends(get_current_user) throwing err as TypeError: 'Depends' object is not subscriptable
    attempts = user.get("attempts", 0)
    if attempts >= MAX_ATTEMPTS:
        if "attempt_time" in user and datetime.now() - user["attempt_time"] < timedelta(hours=24):
            logger.warning("Max attempts reached")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Maximum attempts reached. Try again after 24 hours.")
        else:
            collection.update_one({"_id": user["_id"]}, {"$set": {"attempts": 0, "attempt_time": None}})
            attempts = 0

    if not HASHING.verify(data.password,user["password"]):
        collection.update_one(
        {"_id": user["_id"]}, {"$set": {"attempts": attempts + 1,"attempt_time":datetime.now()}}
        )
        logger.info("old password is incorrect")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password is incorrect")
    
    if user["status"] != "Active":
        logger.info("status is inactive")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please login to change your password")
    if data.password==data.new_password:
        logger.info("old and new password are same")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="New password must be different from the old password")

    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",data.new_password):
        logger.info("password is invalid")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one capital letter, one small letter, one digit, one special character, and be at least 8 characters long")
    hashed_new_password = HASHING.hash(data.new_password)
    collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
                "password": hashed_new_password,
                "password_updated_at": datetime.now()
            }
        }
    )
    logger.info("password changed")
    return {"message": "Password changed successfully"}

async def send_link(request:Request):
    link=request.url_for("reset_password")
    logger.info("link generated to change password")
    return str(link)
@app.post("/reset")
async def reset_password(data:Reset,token:str):
    user=collection.find_one({"username":data.username})
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="token is reqire")
    if data.new_password!=data.confirm_password:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="both fields must be same")
    hashed_new_password = HASHING.hash(data.new_password)
    collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
                "password": hashed_new_password,
                "password_updated_at": datetime.now()
            }
        }
    )
    return {"message":"Password changed successfully.Try log in with new password"}

@handle_exceptions
@app.post("/forget_password")
async def forget_password(data:Forgotted,request:Request,user:dict=Depends(get_current_user)):
    to_email=user.get("username")

    if not mail or not app_password:
        logger.info("email/password are none")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Email or app password is not set in environment variables.")
    
    from_email=mail    #  jee***************@gmail.com
    password=app_password #   ****************
    body=await send_link(request)

    msg=EmailMessage()
    msg.set_content(body)
    msg["Subject"]=data.subject
    msg["From"]=from_email
    msg["To"]=to_email

    with smtplib.SMTP_SSL("smtp.gmail.com",465)as smtp:
        smtp.login(from_email,password)
        smtp.send_message(msg)

    token = f"token-{random.randint(1000, 9999)}"
    logger.info("email sent")
    return {"message":"Email sent successfully","token":token}

@handle_exceptions
@app.post("/logout")
async def log_out(token:str=Depends(oauth2_scheme),user:dict=Depends(get_current_user)):
    username=user.get("username")
    payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    user_name=payload.get("username")
    if username!=user_name:
        logger.error("token is invalid or expired")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Entered token is invalid or token expired" )
    token_black_list.append(token)
    collection.update_one(
    {"_id": user["_id"]},
    {"$set": {"status": "Inactive"}}
    )
    logger.info("user logged out")
    return {"message":"user_logged_out successfully"}


    
