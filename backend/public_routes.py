# backend/public_routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, EmailStr
import json
from bson import ObjectId
from database import get_db
from limiter import limiter

# Create the router
public_router = APIRouter()

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


@public_router.get("/hackathons")
async def read_hackathons(db = Depends(get_db)):
    collection = db.hackathons
    hackathons = list(collection.find({}))
    hackathons_json = json.dumps(hackathons, cls=JSONEncoder)
    return JSONResponse(content=json.loads(JSONEncoder().encode(hackathons)))

@public_router.post("/submit-email")
@limiter.limit("3/minute")
async def submit_email(submission: EmailSubmission, request: Request, db = Depends(get_db)):
    result = db.emails.insert_one({
        "email": submission.email,
        "timestamp": datetime.now()
    })
    if result.inserted_id:
        return {"message": "Email submitted successfully"}
    raise HTTPException(status_code=500, detail="Failed to submit email")

@public_router.post("/submit-hackathon")
@limiter.limit("5/minute")
async def submit_hackathon(submission: HackathonSubmission, request: Request, db = Depends(get_db)):
    result = db.hackathon_suggestions.insert_one({
        "hackathon": submission.hackathon,
        "handled": submission.handled,
        "timestamp": datetime.now()
    })
    if result.inserted_id:
        return {"message": "Hackathon submitted successfully"}
