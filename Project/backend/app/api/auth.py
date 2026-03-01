# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import get_database
from app.schemas.auth import LoginRequest, RegisterRequest, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token, verify_token
from datetime import datetime
from bson import ObjectId
import logging

router = APIRouter(prefix="/auth", tags=["authentication"])
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterRequest, db=Depends(get_database)):
    """Register a new user"""
    # Check if user exists
    if await db.users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if await db.users.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user_dict = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "full_name": user_data.full_name,
        "department": user_data.department,
        "station": user_data.station,
        "role": "user",
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    user_dict["id"] = str(result.inserted_id)
    
    # Remove password before returning
    user_dict.pop("hashed_password", None)
    
    return user_dict

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db=Depends(get_database)):
    """Login user"""
    user = await db.users.find_one({"email": login_data.email})
    
    if not user or not verify_password(login_data.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Account is disabled")
    
    # Update last login
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create token
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": access_token,  # Simplified for now
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    """Get current user info"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user["id"] = str(user["_id"])
    user.pop("hashed_password", None)
    
    return user