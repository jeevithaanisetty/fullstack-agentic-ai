import requests
import random
import json
import re
from app.core.config import NEWS_API_KEY,NEWS_API_URL,ARTICLE_COUNT,KEYWORD,GEMINI_API_KEY,TAVILY_API_KEY
from datetime import datetime, timedelta 
from app.database.db import db
from app.models.polls import PollCreate
from app.utils.decorator import handle_exceptions
from app.utils.logger import get_logger
import google.generativeai as genai
from tavily import TavilyClient

logger=get_logger("polling_api.main")

genai.configure(api_key="AIzaSyCnXEIs0501K4LD5Lkd6hr66S508RqOjsk")
model=genai.GenerativeModel("gemini-2.5-flash")
# tavily
client=TavilyClient(api_key=TAVILY_API_KEY)

async def tavily_searching(query):
    url="https://api.tavily.com/search"
    response=client.search(query=query,search_depth="basic")
    result_urls=[item["url"] for item in response["results"]]
    print(result_urls)
    logger.info("related content is found with tavily search")
    return result_urls

async def summarize_article(article):
    prompt=f"Summarize this news article in 2 lines:\n\nTitle:{article["title"]}\n\nContent:{article.get("content","")}"
    response=model.generate_content(prompt)
    print(response.text)
    logger.info("article is summarized using genai")
    return response.text.strip()

@handle_exceptions
async def fetch_news_articles():
    now = datetime.utcnow()
    from_time = (now - timedelta(hours=96)).isoformat("T") + "Z"
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
async def create_poll_service(data,source_url=None):
    expires_at = datetime.utcnow() + timedelta(hours=24)
    options = [{"text": opt, "votes": 0} for opt in (data.options)]

    new_poll = {
        "question": data.question,
        "options": options,
        "voted_users": [],
        "expires_at": expires_at,
        "is_active": True,
        "summary":data.summary,
        "related_content":data.related_info,
        "source_url": source_url
    }
    result =await db.polls.insert_one(new_poll)
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
    articles=await fetch_news_articles()
    for article in articles:
        title = article.get("title")
        content=article.get("content","")
        if not title:
            continue
        prompt = f"""Generate a poll question and options about this news:
                    {title}

                    Return only valid JSON in the format:
                    {{
                    "question": "<your question>",
                    "options": ["Option1", "Option2", "Option3", "Option4"]
                    }}
                    Do not include any text outside JSON.
                    """
        response=model.generate_content(prompt)
        ai_output=response.text   #str
        #print(type(ai_output))
        try:
            output=json.loads(ai_output)  #dict
            #print(type(output))
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', ai_output, re.DOTALL)
            if match:
                try:
                    output = json.loads(match.group())
                except json.JSONDecodeError:
                    print("Still invalid JSON:", match.group())

        question=output.get("question",f"Do you agree with this news? {title}")
        options=output.get("options",["Agree", "Disagree","Neutral","None"])
        
        article_summary=await summarize_article(article)
        tavily_response=await tavily_searching(article["title"])

        poll_info= PollCreate(
            question=question,
            options=options,
            duration_minutes=1440,  # default 24 hours 
            summary=article_summary,
            related_info=tavily_response
        )
        url = article.get("url")
        existing = db.polls.find_one({"$or": [{"question": question}, {"source_url": url}]})
        if existing:
            continue
        created = create_poll_service(poll_info, source_url=article.get("url"))
        created_polls.append(created)
    return created_polls

