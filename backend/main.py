from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pymongo import MongoClient
import os
import json
from bson import ObjectId
from datetime import datetime
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import uvicorn
from settings import settings


env_path = '.env'
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
    print("Loaded environment from .env file")
else:
    print("No .env file found, using system environment variables")

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
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

# Custom JSON Encoder for MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class EmailSubmission(BaseModel):
    email: EmailStr


class HackathonSubmission(BaseModel):
    hackathon: str
    handled: bool = False


@app.get("/api/hackathons")
async def read_hackathons():
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.mongodb_database]
    collection = db.hackathons
    hackathons = list(collection.find({}))
    print(hackathons)
    client.close()
    hackathons_json = json.dumps(hackathons, cls=JSONEncoder)
    print(hackathons_json)
    return JSONResponse(content=json.loads(JSONEncoder().encode(hackathons)))


@app.post("/api/submit-email")
@limiter.limit("3/minute")
async def submit_email(submission: EmailSubmission, request: Request):
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.mongodb_database]

    result = db.emails.insert_one({
        "email": submission.email,
        "timestamp": datetime.now()
    })
    if result.inserted_id:
        return {"message": "Email submitted successfully"}
    raise HTTPException(status_code=500, detail="Failed to submit email")


@app.post("/api/submit-hackathon")
@limiter.limit("5/minute")
async def submit_hackathon(submission: HackathonSubmission, request: Request):
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.mongodb_database]

    result = db.hackathon_suggestions.insert_one({
        "hackathon": submission.hackathon,
        "handled": submission.handled,
        "timestamp": datetime.now()
    })
    if result.inserted_id:
        return {"message": "Hackathon submitted successfully"}
    raise HTTPException(status_code=500, detail="Failed to submit hackathon")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
