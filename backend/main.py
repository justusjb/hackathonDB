from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
import json
from bson import ObjectId

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
