from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from settings import settings
from database import get_db

api_key_scheme = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

scraping_router = APIRouter()

@scraping_router.get("/start", dependencies=[Depends(get_api_key)])
async def start_scrape(db = Depends(get_db)):
    # Placeholder for scraping logic
    return JSONResponse(content={"status": "Scraping initiated"})

@scraping_router.get("/status", dependencies=[Depends(get_api_key)])
async def scrape_status(db = Depends(get_db)):
    # Placeholder for scraping status
    return JSONResponse(content={"status": "Scraping in progress"})