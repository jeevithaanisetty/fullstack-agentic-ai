import requests
import logging
from core.config import NEWS_API_KEY,NEWS_API_URL,ARTICLE_COUNT
from db.database import db
from services.poll_service import create_poll_service, poll_creation
from models.poll import PollCreate

async def get_news_articles():
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

async def create_poll():
    created_polls=[]
    articles=get_news_articles()
    for article in articles:
        question = f"Do you agree with this news? {article['title']}"
        poll_info= PollCreate(
            question=question,
            options={"A":"Agree","B": "Disagree", "C":"Neutral","D":"None"},
            duration_minutes=1440  # default 24 hours
        )     
        existing = await db.polls.find_one({"question": question})
        if existing:
            continue
        created = await poll_creation(poll_info, user_id="system", source_url=article.get("url"))   # ?
        created_polls.append(created)
    return created_polls
