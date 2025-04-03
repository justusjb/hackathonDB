from pydantic import BaseModel, EmailStr, Field, field_serializer, SerializationInfo
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
url
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

    @field_serializer('start_date', 'end_date')
    def serialize_datetime(self, dt: datetime, info: SerializationInfo) -> str | datetime:
        return dt.isoformat() if info.mode == 'json' else dt  # only serializing when json is requested is a workaround to ensure that dates are date objects in the MongoDB and not strings.


class HackathonStatus(str, Enum):
    ANNOUNCED = "announced"
    APPLICATIONS_OPEN = "applications_open"
    APPLICATIONS_CLOSED = "applications_closed"
    EXPECTED = "expected"


class HackathonBase(BaseModel):
    name: str
    date: DateRange
    location: Location
    url: str
    notes: Optional[str] = None
    status: HackathonStatus


class Hackathon(HackathonBase):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
    
    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime, info: SerializationInfo) -> str | datetime:
        return dt.isoformat() if info.mode == 'json' else dt  # only serializing when json is requested is a workaround to ensure that dates are date objects in the MongoDB and not strings.

    # Method to convert to MongoDB dictionary
    def to_mongo(self) -> Dict[str, Any]:
        # Convert to dict that MongoDB can store
        data = self.model_dump(by_alias=True, exclude={"id"}, mode='python')
        if self.id:
            data["_id"] = self.id
        return data
    
    # Method to convert from MongoDB document
    @classmethod
    def from_mongo(cls, data: Dict[str, Any]) -> "Hackathon":
        if "_id" in data and data["_id"]:
            # Convert MongoDB ObjectId to string
            data["_id"] = str(data["_id"])
        return cls.model_validate(data)

    @classmethod
    def safe_from_mongo(cls, data: Dict[str, Any]) -> Optional["Hackathon"]:
        try:
            return cls.from_mongo(data)
        except Exception as e:
            print(f"Error parsing hackathon: {e}")
            return None
