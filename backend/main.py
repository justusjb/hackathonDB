from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os
import json
from bson import ObjectId
from datetime import datetime


# print current working directory
print(os.getcwd())

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOCAL_DEV = os.getenv("LOCAL_DEV", False) == "True"
print(f"LOCAL_DEV: {LOCAL_DEV}")


# Custom JSON Encoder for MongoDB ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


@app.get("/api/hackathons")
async def read_hackathons():
    client = MongoClient(os.environ['MONGODB_URI'])
    db = client.hackathons_test_1
    collection = db.hackathons
    hackathons = list(collection.find({}))
    print(hackathons)
    client.close()
    hackathons_json = json.dumps(hackathons, cls=JSONEncoder)
    print(hackathons_json)
    return JSONResponse(content=json.loads(JSONEncoder().encode(hackathons)))


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if LOCAL_DEV:
    @app.get("/", response_class=HTMLResponse)
    async def read_form(request: Request):
        return templates.TemplateResponse("submit_hackathons.html", {"request": request})


    @app.post("/submit")
    async def submit_form(request: Request):
        client = MongoClient(os.environ['MONGODB_URI'])
        db = client.hackathons_test_1
        collection = db.hackathons
        try:
            data = await request.json()
            name = data['name']
            date_str = data['date']
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            hackathon = {
                "name": name,
                "date": date_obj
            }
            collection.insert_one(hackathon)
            return {"message": "Hackathon added successfully!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
