from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime

"""
Database structure:

Hackathon object
(MongoDB ID)
name
date
  start_date
  end_date
location
  city
  state
  country
  coordinates
      lat
      long
URL
Notes
status
created_at
"""

class EmailSubmission(BaseModel):
    email: EmailStr


class HackathonSubmission(BaseModel):
    hackathon: str
    handled: bool = False


class Coordinates(BaseModel):
    lat: float
    long: float


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str
    coordinates: Coordinates


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime


class HackathonStatus(str, Enum):
    ANNOUNCED = "announced"
    APPLICATIONS_OPEN = "applications_open"
    APPLICATIONS_CLOSED = "applications_closed"
    EXPECTED = "expected"


class HackathonBase(BaseModel):
    name: str
    date: DateRange
    location: Location
    url: str = Field(alias='URL') # UPDATE THIS as part of migration from URL to url. just use "url: str"
    notes: Optional[str] = None
    status: HackathonStatus


class Hackathon(HackathonBase):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        # Allow MongoDB _id to be used
        allow_population_by_field_name = True
        # Make model work with MongoDB
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
    
    # Method to convert to MongoDB dictionary
    def to_mongo(self) -> Dict[str, Any]:
        # Convert to dict that MongoDB can store
        data = self.dict(by_alias=True, exclude={"id"})
        if self.id:
            data["_id"] = self.id
        return data
    
    # Method to convert from MongoDB document
    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> "Hackathon":
        if "_id" in data and data["_id"]:
            # Convert MongoDB ObjectId to string
            data["_id"] = str(data["_id"])
        return cls.parse_obj(data)
