# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    department: Optional[str] = None
    station: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str
    full_name: Optional[str] = None
    department: Optional[str] = None
    station: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True