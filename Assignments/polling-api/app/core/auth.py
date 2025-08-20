from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import datetime,timedelta
from core.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRE_TIME
from data.db import db
from bson import ObjectId

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    payload={"sub":data["user_id"],"exp":(datetime.utcnow()+timedelta(minutes=TOKEN_EXPIRE_TIME))}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_loggedin_user(token:str=Depends(oauth2_scheme)):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_id=payload.get("sub")
    if user_id is None:
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    user= await db.users.find_one({"_id":ObjectId(user_id)})
    if user is None:
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    return user