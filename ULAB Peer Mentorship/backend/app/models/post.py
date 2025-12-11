from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

# Helper to convert MongoDB ObjectId to str
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

# Post model stored in MongoDB
class Post(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: str = Field(...)        # ID of the user who posted
    user_name: str = Field(...)      # Name of the user
    text: str = Field(...)           # Post content
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved: bool = Field(default=False)  # For admin approval

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

# Model used for creating a post
class PostCreate(BaseModel):
    text: str
