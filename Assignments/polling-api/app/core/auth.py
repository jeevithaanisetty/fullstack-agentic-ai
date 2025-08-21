from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import datetime,timedelta
from app.core.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRE_TIME
from app.database.db import db
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

logger=get_logger("polling_api.main")

@handle_exceptions
def create_token(data):
    payload={"sub":data,"exp":(datetime.utcnow()+timedelta(minutes=TOKEN_EXPIRE_TIME))}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    logger.info("token is generated")
    return token

@handle_exceptions
async def get_loggedin_user(token:str=Depends(oauth2_scheme)):
    try:
        if not token:
            logger.error("Token is required for authentication")
            raise HTTPException(status_code=400,detail="User should be authenticated before polling vote.Provide your token")
    except JWTError as e:
        logger.warning("token is invalid or expired")
        raise HTTPException(status_code=401,detail="token is invalid or expired")
    
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_email=payload.get("sub")
    if user_email is None:
        logger.error("Invalid token")
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    user= db.users.find_one({"email":(user_email)})
    if user is None:
        logger.info("Couldn't find any user with this token.Check token again")
        raise HTTPException(stutus_code=401,detail="Invalid Credentials")
    return user