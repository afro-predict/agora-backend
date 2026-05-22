from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agents.market_creation_agent import run_market_creation
from agents.probability_agent import run_probability_updates
from agents.resolution_agent import run_market_resolution
import asyncio

scheduler = AsyncIOScheduler()

def create_markets_job():
    print("CRON: Triggering Market Creation Job")
    asyncio.create_task(asyncio.to_thread(run_market_creation))

def update_probabilities_job():
    print("CRON: Triggering Probability Update Job")
    asyncio.create_task(asyncio.to_thread(run_probability_updates))

def run_resolution_job():
    print("CRON: Triggering Resolution Job")
    asyncio.create_task(asyncio.to_thread(run_market_resolution))

def start_scheduler():
    if not scheduler.running:
        print("Starting APScheduler...")
        # Market Creation: Every day at 07:00 WAT (06:00 UTC)
        scheduler.add_job(create_markets_job, 'cron', hour=6, minute=0, id='market_creation')
        
        # Probability Updates: Every 6 hours
        scheduler.add_job(update_probabilities_job, 'interval', hours=6, id='probability_update')
        
        # Run resolution checks every 30 minutes
        scheduler.add_job(run_resolution_job, 'interval', minutes=30)
        
        scheduler.start()
        print("APScheduler started successfully.")

def shutdown_scheduler():
    if scheduler.running:
        print("Shutting down APScheduler...")
        scheduler.shutdown()
