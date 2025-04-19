from database import get_db
from fastapi import FastAPI, Security, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from public_routes import public_router
from scraping_routes import scraping_router
import uvicorn
from limiter import limiter
from settings import settings
import logging

app = FastAPI()

# Set up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public_router, prefix="/api")
app.include_router(scraping_router, prefix="/scraping")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

"""
!!!
From here on temporary code to toggle backend database. 
Remove this once migrated to automated scraping from deployed backend
!!!
"""
api_key_scheme = APIKeyHeader(name="X-API-Key")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_api_key(api_key: str = Security(api_key_scheme)):
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/set-environment", dependencies=[Depends(get_api_key)])
async def set_environment(req: Request):
    data = await req.json()
    environment = data.get("environment")
    if environment not in ("staging", "production"):
        raise HTTPException(status_code=400, detail="Invalid environment")
    # Update the backend's environment (in-memory or persistent)
    settings.update_environment(environment)

    db = get_db()
    actual_db_name = db.name
    expected_db_name = settings.mongodb_database
    logger.info(f"New db: {expected_db_name}, {actual_db_name}")
        
    # Verify we're connected to the expected database
    if actual_db_name != expected_db_name:
        raise Exception(f"Database switch failed: Connected to {actual_db_name} instead of {expected_db_name}")
    return {"status": "success", "environment": environment}


def get_current_db_name(db = Depends(get_db)):
    return {
        "database": db.name,
    }
"""
!!!
End of temporary code to toggle backend database. 
Remove this once migrated to automated scraping from deployed backend
!!!
""" 

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)