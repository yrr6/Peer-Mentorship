# backend/app/models/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

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

# User model stored in MongoDB
class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)  # hashed password
    role: str = Field(default="user")  # user/admin/mentor

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Model used for registration input
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Model used for login input
class UserLogin(BaseModel):
    email: EmailStr
    password: str
