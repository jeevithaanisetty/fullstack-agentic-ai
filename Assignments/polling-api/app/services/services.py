import requests
import logging
from app.core.config import NEWS_API_KEY,NEWS_API_URL,ARTICLE_COUNT
from datetime import datetime, timedelta
from app.database.db import db
from app.models.polls import PollCreate

def fetch_news_articles():
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

async def article_to_poll():
    created_polls=[]
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
        existing = db.polls.find_one({"question": question})
        if existing:
            continue
        created = await create_poll_service(poll_info, source_url=article.get("url"))  #user_id="system"
        created_polls.append(created)
    return created_polls



# async def create_poll( token:str,current_user: dict = Depends(get_loggedin_user)):
#     created_polls = await article_to_poll(current_user["_id"])
#     return [p.to_dict() for p in created_polls]
 
