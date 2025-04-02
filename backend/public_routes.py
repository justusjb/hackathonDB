# backend/public_routes.py
from fastapi import APIRouter, Depends, Request, HTTPException
from datetime import datetime
from database import get_db
from limiter import limiter
from models import Hackathon, EmailSubmission, HackathonSubmission

# Create the router
public_router = APIRouter()

@public_router.get("/hackathons")
async def read_hackathons(db = Depends(get_db)):
    collection = db.hackathons
    hackathons = [Hackathon.from_mongo(doc) for doc in collection.find({})]
    return hackathons


@public_router.post("/submit-email")
@limiter.limit("3/minute")
async def submit_email(submission: EmailSubmission, request: Request, db = Depends(get_db)):
    data = submission.dict()
    data["timestamp"] = datetime.now()
    result = db.emails.insert_one(data)
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


@public_router.post("/submit-hackathon")
@limiter.limit("5/minute")
async def submit_hackathon(submission: HackathonSubmission, request: Request, db = Depends(get_db)):
    data = submission.dict()
    data["timestamp"] = datetime.now()
    result = db.hackathon_suggestions.insert_one(data)
    if result.inserted_id:
        return {"message": "Hackathon submitted successfully"}
    raise HTTPException(status_code=500, detail="Failed to submit hackathon")
