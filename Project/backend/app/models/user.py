# app/models/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from app.utils.helpers import PyObjectId  # Import from helpers

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = None
    department: Optional[str] = None
    station: Optional[str] = None
    role: str = Field(default="user")
    is_active: bool = True
    is_verified: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    refresh_token: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

class UserResponse(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )