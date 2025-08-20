from passlib .context import CryptContext

hashing_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashing_password(password:str) ->str:
    return hashing_context.hash(password)

def verify_password(plain:str,hashed:str)->bool:
    return hashing_context.verify(plain,hashed)