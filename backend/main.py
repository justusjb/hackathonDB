from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_featureflags import FeatureFlags, feature_flag, feature_enabled
from pymongo import MongoClient
import os
import json
from bson import ObjectId
from datetime import datetime

app = FastAPI()
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


@feature_flag("LOCAL_DEV")
@app.post("/api/hackathons")
def insert_hackathon(hackathon):
    client = MongoClient(os.environ['MONGODB_URI'])
    db = client.hackathons_test_1
    collection = db.hackathons
    hackathon_id = collection.insert_one(hackathon).inserted_id
    client.close()
    return hackathon_id


@feature_flag("LOCAL_DEV")
@app.get("/", response_class=HTMLResponse)
async def read_form():
    return """
    <form action="/submit" method="post">
        <label for="name">Hackathon Name:</label><br>
        <input type="text" id="name" name="name"><br>
        <label for="date">Date (YYYY-MM-DD):</label><br>
        <input type="text" id="date" name="date"><br><br>
        <input type="submit" value="Submit">
    </form>
    """


@feature_flag("LOCAL_DEV")
@app.post("/submit")
async def submit_form(name: str = Form(...), date: str = Form(...)):
    client = MongoClient(os.environ['MONGODB_URI'])
    db = client.hackathons_test_1
    collection = db.hackathons
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        hackathon = {
            "name": name,
            "date": date_obj
        }
        collection.insert_one(hackathon)
        return {"message": "Hackathon added successfully!"}
    except Exception as e:
        return {"error": str(e)}
