from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.services import fetch_news_articles
import logging
 
scheduler = AsyncIOScheduler()
 
def start_scheduler():
    scheduler.add_job(fetch_news_job, "interval", hours=24)
    scheduler.start()
    logging.info("Scheduler started")
 
async def fetch_news_job():
    try:
        polls = await fetch_news_articles()
        logging.info(f"Created {len(polls)} polls from news")
    except Exception as e:
        logging.error(f"Error in news part: {e}")