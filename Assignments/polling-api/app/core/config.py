import os
import random
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL","mongodb://localhost:27017/")
DATABASE_NAME=os.getenv("DB_NAME","polls_info")

LOG_FILE=Path("logs/polling_api")

NEWS_API_KEY=os.getenv("NEWS_API_KEY")
NEWS_API_URL="https://newsapi.org/v2/everything"
keywords = [
    "technology", "science", "politics", "health", "education",
    "space", "finance", "economy", "climate", "cybersecurity",
    "sports", "elections", "startups", "mental health"
]
KEYWORD = random.choice(keywords)
ARTICLE_COUNT=15

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
TOKEN_EXPIRE_TIME=30

GEMINI_API_KEY= "AIzaSyCnXEIs0501K4LD5Lkd6hr66S508RqOjsk" #os.getenv("GEMINI-API-KEY")
TAVILY_API_KEY= os.getenv("TAVILY-API-KEY")

