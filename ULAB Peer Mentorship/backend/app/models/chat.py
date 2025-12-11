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

# Chat message stored in MongoDB
class ChatMessage(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    sender_id: str = Field(...)       # ID of the sender
    sender_name: str = Field(...)     # Name of the sender
    message: str = Field(...)         # Chat message content
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

# Model for sending a chat message via API/WebSocket
class ChatMessageCreate(BaseModel):
    sender_id: str
    sender_name: str
    message: str
