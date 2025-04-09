from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from opencage.geocoder import OpenCageGeocode
import uvicorn
from settings import settings
import httpx
import os
from shared_models import Hackathon, HackathonStatus, Location, Coordinates, DateRange
from database import get_db

app = FastAPI()

geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("admin_panel.html", {"request": request})


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

    components = all_city_data.get('components', {})
    geometry = all_city_data.get('geometry', {})
    
    return Location(
        city=components['_normalized_city'],
        state=components.get('state'),  # Using get because state is optional 
        country=components['country'],
        coordinates=Coordinates(
            lat=geometry['lat'],
            long=geometry['lng']
        )
    )


@app.post("/submit")
async def submit_form(request: Request, db = Depends(get_db)):
    collection = db.hackathons
    try:
        data = await request.json()

        # Handle date
        dates = data['date-range'].split(" to ")
        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")

        # Handle city
        input_city = data['city']
        location = get_city_data(input_city)

        # Build date range model
        date_range = DateRange(
            start_date=start_date,
            end_date=end_date
        )

        # Create the Hackathon object
        hackathon = Hackathon(
            name=data['name'],
            date=date_range,
            location=location,
            url=data['url'],
            notes=data.get('notes', ''),
            status=HackathonStatus(data['status']),
        )

        db_id = collection.insert_one(hackathon.to_mongo())
        return {"message": f"Hackathon added successfully!<br>City: {location.city}<br>State: {location.state}<br>Country: {location.country}"
                            f"<br>ID of the inserted document: {db_id.inserted_id}"}
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/trigger-scrape")
async def trigger_scrape():
    """
    Trigger a new scraping run by calling the backend's trigger endpoint.
    This endpoint is designed to be called from the admin panel's "Run Scrapers" button.
    """
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{backend_url}/scraping/trigger",
                headers={"X-API-Key": settings.ADMIN_API_KEY},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        # Handle specific HTTP errors (like rate limiting or already running)
        status_code = e.response.status_code
        try:
            error_data = e.response.json()
            error_message = error_data.get("message", str(e))
        except:
            error_message = str(e)
        
        raise HTTPException(status_code=status_code, detail=error_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to backend: {str(e)}")


@app.get("/inbox")
async def get_inbox_items(status: str | None = None, db = Depends(get_db)):
    """
    Get all items from the inbox collection with optional status filtering.
    """
    try:
        # Get the inbox collection
        collection = db.inbox
        
        # Build the query based on status parameter
        query = {}
        if status:
            query["review_status"] = status.lower()
        
        # Fetch all matching documents
        cursor = collection.find(query)
        
        # Convert cursor to list and process items
        items = []
        for doc in cursor:
            # Convert ObjectId to string for JSON serialization
            doc['_id'] = str(doc['_id'])
            # Convert datetime objects to ISO format strings
            if 'date' in doc and doc['date']:
                if 'start_date' in doc['date']:
                    doc['date']['start_date'] = doc['date']['start_date'].isoformat()
                if 'end_date' in doc['date']:
                    doc['date']['end_date'] = doc['date']['end_date'].isoformat()
            items.append(doc)
        
        return {
            "status": "success",
            "data": items,
            "count": len(items)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inbox items: {str(e)}")


@app.post("/toggle-database")
async def toggle_database(request: Request):
    """
    Toggle between staging and production database environments.
    This endpoint updates the ENVIRONMENT setting and all subsequent
    database operations will use the new environment.
    """
    try:
        data = await request.json()
        new_environment = data.get("environment")
        
        # Validate the environment value
        if new_environment not in ["production", "staging"]:
            raise ValueError("Environment must be either 'production' or 'staging'")
        
        # Skip if the environment is already set to the requested value
        if settings.ENVIRONMENT == new_environment:
            return {
                "success": True,
                "message": f"Already using {new_environment} environment",
                "current_environment": new_environment,
                "database": settings.mongodb_database
            }
        
        # Update the environment setting
        settings.update_environment(new_environment)
        
        # Verify that the environment setting was actually updated
        if settings.ENVIRONMENT != new_environment:
            raise Exception(f"Environment update failed: Still set to {settings.ENVIRONMENT}")

        db = get_db()
        # Check which database we're actually connected to
        actual_db_name = db.name
        expected_db_name = settings.mongodb_database
        
        # Verify we're connected to the expected database
        if actual_db_name != expected_db_name:
            raise Exception(f"Database switch failed: Connected to {actual_db_name} instead of {expected_db_name}")
        
        return {
            "success": True,
            "message": f"Switched to {new_environment} environment",
            "current_environment": new_environment,
            "database": actual_db_name
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle database: {str(e)}")


@app.get("/current-environment")
async def get_current_environment(db = Depends(get_db)):
    """
    Get the current database environment and database name.
    """
    return {
        "environment": settings.ENVIRONMENT,
        "database": db.name,
        "is_production": settings.is_production,
        "is_testing": settings.is_testing
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
