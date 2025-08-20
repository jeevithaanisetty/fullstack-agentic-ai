import requests
import logging
from core.config import NEWS_API_KEY,NEWS_API_URL,ARTICLE_COUNT
from datetime import datetime, timedelta
from db.database import db
from services.poll_service import create_poll_service, poll_creation
from models.poll import PollCreate

async def fetch_news_articles():
    logging.info ("getting news articles from web....wait")
    news_api =  requests.get(
        NEWS_API_URL, params = {
        "apiKey" :NEWS_API_KEY,
        "domains" : "wsj.com",
        "pageSize" : ARTICLE_COUNT
    }
    )
    news_api.raise_for_status()
    news_articles = news_api.json().get("articles", [])
    logging.info (f"\nFetched {len(news_articles)} articles\n")
    print(f"total articles fetched:{len(news_articles)}")
    return news_articles

async def article_to_poll():
    created_polls=[]
    articles=fetch_news_articles()
    for article in articles:
        question = f"Do you agree with this news? {article['title']}"
        poll_info= PollCreate(
            question=question,
            options=["Agree", "Disagree","Neutral","None"],
            duration_minutes=1440  # default 24 hours
        )     
        existing = await db.polls.find_one({"question": question})
        if existing:
            continue
        created = await create_poll_service(poll_info, source_url=article.get("url"))  #user_id="system"
        created_polls.append(created)
    return created_polls

async def create_poll_service(data, source_url=None):
    expires_at = datetime.utcnow() + timedelta(hours=24)
    options = [{i: opt, "votes": 0} for i,opt in enumerate(data.options,1)]
 
    new_poll = {
        "question": data.question,
        "options": options,
        "voted_users": [],
        "expires_at": expires_at,
        "is_active": True,
        "source_url": source_url
    }
    result = await db.polls.insert_one(new_poll)
    return await db.polls.find_one({"_id": result.inserted_id})    #return result
