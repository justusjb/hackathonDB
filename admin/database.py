from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database
from fastapi import HTTPException
from settings import settings

# Initialize clients as None - they will be created on first use
_async_client: Optional[AsyncIOMotorClient] = None
_sync_client: Optional[MongoClient] = None

def get_async_client() -> AsyncIOMotorClient:
    """
    Get or create the async MongoDB client.
    Uses singleton pattern to avoid creating multiple connections.
    """
    global _async_client
    if _async_client is None:
        _async_client = AsyncIOMotorClient(settings.MONGODB_URI)
    return _async_client

def get_sync_client() -> MongoClient:
    """
    Get or create the synchronous MongoDB client.
    Uses singleton pattern to avoid creating multiple connections.
    """
    global _sync_client
    if _sync_client is None:
        try:
            _sync_client = MongoClient(settings.MONGODB_URI)
            # Verify sync connection works immediately
            _sync_client.admin.command('ping')
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not connect to MongoDB: {str(e)}"
            )
    return _sync_client

def get_async_db() -> AsyncIOMotorDatabase:
    """
    Get the async database instance.
    For use with FastAPI endpoints and other async contexts.
    """
    return get_async_client()[settings.mongodb_database]

def get_db() -> Database:
    """
    Get the synchronous database instance.
    For use with synchronous contexts or background tasks.
    """
    return get_sync_client()[settings.mongodb_database]

async def close_async_connection():
    """
    Close the async MongoDB connection.
    Should be called when the application shuts down.
    """
    global _async_client
    if _async_client is not None:
        _async_client.close()
        _async_client = None

def close_sync_connection():
    """
    Close the synchronous MongoDB connection.
    Should be called when the application shuts down.
    """
    global _sync_client
    if _sync_client is not None:
        _sync_client.close()
        _sync_client = None

def init_db(app):
    """
    Initialize database connections and register startup/shutdown handlers.
    Call this when starting your FastAPI application.
    
    Example:
        app = FastAPI()
        init_db(app)
    """
    @app.on_event("startup")
    async def verify_async_connection():
        """Verify async database connection on startup"""
        try:
            # Get client and verify connection works
            client = get_async_client()
            await client.admin.command('ping')
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Could not connect to MongoDB: {str(e)}"
            )

    @app.on_event("shutdown")
    async def shutdown_db_clients():
        """Cleanup database connections on shutdown"""
        await close_async_connection()
        close_sync_connection()
