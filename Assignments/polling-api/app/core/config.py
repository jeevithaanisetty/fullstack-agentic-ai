import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL","mongo://localhost:27017")
DATABASE_NAME=os.getenv("DB_NAME","polling_app")

NEWS_API_KEY=os.getenv("NEWS_API_KEY")

SECRET_KEY=os.getenv("SECRET_KEY","HAappy123!")
ALGORITHM="HS256"
TOKEN_EXPIRE_TIME=30

