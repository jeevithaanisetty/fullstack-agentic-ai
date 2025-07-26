from passlib.context import CryptContext

SECRET_KEY="123@456#"
ALGORITHM="HS256"
EXPIRE_TIME=20
MAX_ATTEMPTS=3
HASHING=CryptContext(schemes=["bcrypt"], deprecated="auto")