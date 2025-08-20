from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime,timedelta
from app.core.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRE_TIME
from app.database.db import db

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_token(data):
    payload={"sub":data,"exp":(datetime.utcnow()+timedelta(minutes=TOKEN_EXPIRE_TIME))}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

async def get_loggedin_user(token:str=Depends(oauth2_scheme)):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_email=payload.get("sub")
    if user_email is None:
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    user= db.users.find_one({"email":(user_email)})
    if user is None:
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    return user