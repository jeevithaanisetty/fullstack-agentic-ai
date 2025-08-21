from passlib .context import CryptContext
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger

hashing_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
logger=get_logger("polling_api.main")

@handle_exceptions
def hashing_password(password:str) ->str:
    logger.info("Password is hashed to save")
    return hashing_context.hash(password)

@handle_exceptions
def verify_password(plain:str,hashed:str)->bool:
    logger.info("Password is verified")
    return hashing_context.verify(plain,hashed)