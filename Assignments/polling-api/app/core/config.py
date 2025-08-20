import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL","mongodb://localhost:27017/")
DATABASE_NAME=os.getenv("DB_NAME","polls_info")

NEWS_API_KEY=os.getenv("NEWS_API_KEY","224aed70fc5e450e93a7b2c745e7efd9")
NEWS_API_URL="https://newsapi.org/v2/everything"
ARTICLE_COUNT=5

SECRET_KEY=os.getenv("SECRET_KEY","HAappy123!")
ALGORITHM="HS256"
TOKEN_EXPIRE_TIME=30

