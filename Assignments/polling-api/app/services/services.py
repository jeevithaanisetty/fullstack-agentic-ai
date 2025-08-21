import requests
import random
from app.core.config import NEWS_API_KEY,NEWS_API_URL,ARTICLE_COUNT,KEYWORD
from datetime import datetime, timedelta 
from app.database.db import db
from app.models.polls import PollCreate
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger

logger=get_logger("polling_api.main")

@handle_exceptions
def fetch_news_articles():
    now = datetime.utcnow()
    from_time = (now - timedelta(hours=48)).isoformat("T") + "Z"
    to_time = now.isoformat("T") + "Z"

    response = requests.get(
        NEWS_API_URL,
        params={
            "apiKey": NEWS_API_KEY,
            "q": KEYWORD,
            "from": from_time,
            "to": to_time,
            "sortBy": "publishedAt",
            "pageSize": ARTICLE_COUNT,
            "page": random.randint(1,5)
        }
    )
    
    response.raise_for_status()
    data = response.json()
    
    total = data.get("totalResults", 0)
    articles = data.get("articles", [])
    
    logger.info(f"Keyword: {KEYWORD}")
    logger.info(f"Total articles available: {total}")
    logger.info(f"Fetched: {len(articles)} articles")

    if not articles:
        logger.warning("No articles found for the given time window and keyword.")
    return articles

@handle_exceptions
async def create_poll_service(data, source_url=None):
    expires_at = datetime.utcnow() + timedelta(hours=24)
    options = [{"text": opt, "votes": 0} for opt in (data.options)]

    new_poll = {
        "question": data.question,
        "options": options,
        "voted_users": [],
        "expires_at": expires_at,
        "is_active": True,
        "source_url": source_url
    }
    result =  db.polls.insert_one(new_poll)
    return db.polls.find_one({"_id": result.inserted_id})    #return result

@handle_exceptions
def delete_expired_polls():
    now = datetime.utcnow()
    result = db.polls.delete_many({"expires_at": {"$lt": now}})
    logger.info(f"Deleted {result.deleted_count} expired polls.")

@handle_exceptions
async def article_to_poll():
    created_polls=[]
    delete_expired_polls()
    articles=fetch_news_articles()
    for article in articles:
        title = article.get("title")
        if not title:
            continue
        question = f"Do you agree with this news? {article['title']}"
        poll_info= PollCreate(
            question=question,
            options=["Agree", "Disagree","Neutral","None"],
            duration_minutes=1440  # default 24 hours
        )
        url = article.get("url")
        existing = db.polls.find_one({"$or": [{"question": question}, {"source_url": url}]})
        if existing:
            continue
        created = await create_poll_service(poll_info, source_url=article.get("url"))
        created_polls.append(created)
    return created_polls

