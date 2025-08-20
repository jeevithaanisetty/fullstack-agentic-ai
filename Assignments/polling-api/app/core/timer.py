from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.news_service import fetch_and_create_polls
import logging
 
scheduler = AsyncIOScheduler()
 
def start_scheduler():
    scheduler.add_job(fetch_news_job, "interval", minutes=30)
    scheduler.start()
    logging.info("Scheduler started")
 
async def fetch_news_job():
    try:
        polls = await fetch_and_create_polls(country="us", limit=5)
        logging.info(f"Created {len(polls)} polls from news")
    except Exception as e:
        logging.error(f"Error in news part: {e}")