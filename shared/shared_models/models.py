from pydantic import BaseModel, EmailStr, Field, field_serializer, SerializationInfo, field_validator, HttpUrl, BeforeValidator
from enum import Enum
from typing import Optional, Dict, Any, Annotated
from datetime import datetime, timezone
from bson import ObjectId

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

PyObjectId = Annotated[
    str,
    BeforeValidator(lambda v: str(v) if isinstance(v, ObjectId) else v)
]

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


class InboxStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class HackathonBase(BaseModel):
    name: str
    date: DateRange
    location: Location
    url: HttpUrl
    notes: Optional[str] = None
    status: HackathonStatus
    source: Optional[str] = None # This is only optional for backwards compatibility. Make this non-optional later.
    application_form: Optional[str] = None
    application_deadline: Optional[datetime] = None

    @field_validator('url', mode='before')
    @classmethod
    def ensure_scheme_in_url(cls, v: str) -> str:
        """Adds 'https://' to the URL if scheme is missing."""
        # Check if v is a string, is not empty, and lacks a scheme
        if isinstance(v, str) and v and not (v.startswith('http://') or v.startswith('https://')):
            return f'https://{v}'
        return v


class InboxItem(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id") # MongoDB ID

    # Fields mirroring HackathonBase, but optional
    name: Optional[str] = None
    date: Optional[DateRange] = None
    location: Optional[str] = None  # Store as simple string for inbox
    url: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[HackathonStatus] = None

    # Inbox-specific metadata
    source_url: Optional[str] = None
    scraper_name: Optional[str] = None
    scraped_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    review_status: InboxStatus = Field(default=InboxStatus.PENDING)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }


class Hackathon(HackathonBase):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }

    @field_serializer('url')
    def serialize_url(self, v: HttpUrl) -> str:
        return str(v)
    
    @field_serializer('created_at', 'application_deadline')
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
