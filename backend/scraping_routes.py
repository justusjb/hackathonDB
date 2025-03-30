from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from settings import settings
from database import get_db

"""
PLACEHOLDER
"""

def admin_only_dependency():
    if not settings.is_production:
        return True
    raise HTTPException(status_code=403, detail="Admin access only available in non-production environment")

scraping_router = APIRouter()

@scraping_router.post("/start", dependencies=[Depends(admin_only_dependency)])
async def start_scrape(db = Depends(get_db)):
    # Placeholder for scraping logic
    return JSONResponse(content={"status": "Scraping initiated"})

@scraping_router.get("/status", dependencies=[Depends(admin_only_dependency)])
async def scrape_status(db = Depends(get_db)):
    # Placeholder for scraping status
    return JSONResponse(content={"status": "Scraping in progress"})