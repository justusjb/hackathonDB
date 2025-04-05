from fastapi import APIRouter, Security, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from settings import settings
from database import get_db
from run_scrapers import run_all_scrapes
import time
from datetime import datetime, timedelta
import logging


api_key_scheme = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Rate limiting setup
last_scrape_time = None
MIN_SCRAPE_INTERVAL = timedelta(minutes=5)  # Minimum time between scrapes

logger = logging.getLogger(__name__)

scraping_router = APIRouter()


@scraping_router.get("/start", dependencies=[Depends(get_api_key)])
async def start_scrape(db = Depends(get_db)):
    # Placeholder for scraping logic
    return JSONResponse(content={"status": "Scraping initiated"})

@scraping_router.get("/status", dependencies=[Depends(get_api_key)])
async def scrape_status(db = Depends(get_db)):
    # Placeholder for scraping status
    return JSONResponse(content={"status": "Scraping in progress"})


# Store the status of the last scraping job
scraping_status = {
    "is_running": False,
    "last_run": None,
    "last_status": None,
    "items_collected": 0
}

def background_scraping():
    """Background task to run the scraping process"""
    global scraping_status
    
    try:
        scraping_status["is_running"] = True
        scraping_status["last_run"] = datetime.now().isoformat()
        scraping_status["last_status"] = "running"
        
        # Run the scraping process
        logger.info("Starting background scraping process")
        run_all_scrapes()
        
        # Update status on completion
        scraping_status["last_status"] = "completed"
        logger.info("Background scraping process completed successfully")
        
    except Exception as e:
        # Log any errors and update status
        logger.error(f"Error in background scraping: {str(e)}", exc_info=True)
        scraping_status["last_status"] = f"failed: {str(e)}"
    
    finally:
        scraping_status["is_running"] = False

@scraping_router.post("/trigger", dependencies=[Depends(get_api_key)])
async def trigger_scrape(background_tasks: BackgroundTasks):
    """
    Trigger a new scraping run if rate limiting allows
    """
    global last_scrape_time
    
    # Check if scraping is already running
    if scraping_status["is_running"]:
        return JSONResponse(
            status_code=409,
            content={
                "status": "error",
                "message": "A scraping job is already in progress"
            }
        )
    
    # Check rate limiting
    current_time = datetime.now()
    if last_scrape_time and (current_time - last_scrape_time) < MIN_SCRAPE_INTERVAL:
        wait_time = (MIN_SCRAPE_INTERVAL - (current_time - last_scrape_time)).seconds
        return JSONResponse(
            status_code=429,
            content={
                "status": "error",
                "message": f"Rate limit exceeded. Please wait {wait_time} seconds before triggering another scrape."
            }
        )
    
    # Update last scrape time and trigger background task
    last_scrape_time = current_time
    background_tasks.add_task(background_scraping)
    
    return JSONResponse(
        content={
            "status": "success",
            "message": "Scraping initiated in background"
        }
    )

@scraping_router.get("/status", dependencies=[Depends(get_api_key)])
async def get_scrape_status():
    """
    Get the current status of the scraping process
    """
    return JSONResponse(content={
        "status": "success",
        "data": {
            "is_running": scraping_status["is_running"],
            "last_run": scraping_status["last_run"],
            "last_status": scraping_status["last_status"]
        }
    })

