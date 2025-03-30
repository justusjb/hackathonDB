from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from datetime import datetime
from opencage.geocoder import OpenCageGeocode
import uvicorn
from settings import settings
import httpx
import os

app = FastAPI()

mongo_client = MongoClient(settings.MONGODB_URI)

def get_db():
    return mongo_client[settings.mongodb_database]

geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("submit_hackathons.html", {"request": request})


def geodata_api_call(query):
    results = geocoder.geocode(query)
    city_index = None
    for i, result in enumerate(results):
        if result['components']['_type'] == 'city':
            city_index = i
            break
    return results[city_index] if city_index is not None else None


def get_city_data(city):

    all_city_data = geodata_api_call(city)

    if all_city_data is None:
        print("City not found. Retrying with prefix:")
        query_prefix = 'city of'
        all_city_data = geodata_api_call(f"{query_prefix} {city}")
        if all_city_data is None:
            raise Exception("City not found")

    if ('geometry' not in all_city_data or 'lat' not in all_city_data['geometry'] or 'lng' not in
            all_city_data['geometry']):
        raise Exception("City coordinates not found. This is a really weird error that is not supposed to happen.")

    if ('components' not in all_city_data or '_normalized_city' not in all_city_data['components'] or
            'country' not in all_city_data['components']):
        raise Exception("City components not found. This is a really weird error that is not supposed to happen.")

    return {"lat": all_city_data['geometry']['lat'],
            "long": all_city_data['geometry']['lng'],
            "city": all_city_data['components']['_normalized_city'],
            "state": all_city_data['components']['state'] if 'state' in all_city_data['components'] else None,
            "country": all_city_data['components']['country']}


@app.post("/submit")
async def submit_form(request: Request, db = Depends(get_db)):
    collection = db.hackathons
    try:
        data = await request.json()

        name = data['name']

        # Handle date
        dates = data['date-range'].split(" to ")
        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")

        # Handle city
        input_city = data['city']
        city_data = get_city_data(input_city)
        city = city_data['city']
        state = city_data['state']
        country = city_data['country']
        lat = city_data['lat']
        long = city_data['long']

        hackathon = {
            "name": name,
            "date": {
                "start_date": start_date,
                "end_date": end_date
            },
            "location": {
                "city": city,
                "state": state,
                "country": country,
                "coordinates": {
                    "lat": lat,
                    "long": long
                }
            },
            "URL": data['URL'],
            "notes": data['notes'],
            "status": data['status'],
            "created_at": datetime.now(),

        }
        db_id = collection.insert_one(hackathon)
        return {"message": f"Hackathon added successfully!<br>City: {city}<br>State: {state}<br>Country: {country}"
                            f"<br>ID of the inserted document: {db_id.inserted_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/test-scraping")
async def test_scraping_access():
    """Test that we can access the secured scraping endpoint"""
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{backend_url}/scraping/start",
                headers={"X-API-Key": settings.ADMIN_API_KEY},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to backend: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
