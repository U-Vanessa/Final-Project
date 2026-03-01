from datetime import datetime
from typing import Any, Dict
from bson import ObjectId
from pydantic import BaseModel, Field
from app.database import db
from app.core.config import settings
from app.core.security import get_password_hash

class PyObjectId(ObjectId):
    """Custom Pydantic type for MongoDB ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

def prepare_update_data(data: BaseModel) -> Dict[str, Any]:
    """Prepare update data by removing None values and adding timestamp"""
    update_data = data.dict(exclude_unset=True)
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    # Add updated_at timestamp
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
    
    return update_data

def serialize_document(doc: Dict) -> Dict:
    """Serialize MongoDB document for JSON response"""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        # Optionally remove _id if you want only id
        # doc.pop("_id", None)
    return doc

async def create_admin_user():
    """Create admin user if it doesn't exist"""
    try:
        # Ensure database is connected
        if db.database is None:
            await db.connect()
        
        admin_exists = await db.database.users.find_one({"email": settings.ADMIN_EMAIL})
        
        if not admin_exists:
            admin_user = {
                "username": settings.ADMIN_USERNAME,
                "email": settings.ADMIN_EMAIL,
                "hashed_password": get_password_hash(settings.ADMIN_PASSWORD),
                "full_name": "System Administrator",
                "department": "IT",
                "station": "Kigali HQ",
                "role": "admin",
                "is_active": True,
                "is_verified": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": None
            }
            
            result = await db.database.users.insert_one(admin_user)
            print(f"✅ Admin user created successfully!")
            print(f"   Email: {settings.ADMIN_EMAIL}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
            print(f"   ID: {result.inserted_id}")
            return True
        else:
            print(f"ℹ️ Admin user already exists: {settings.ADMIN_EMAIL}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

def validate_password_strength(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    # Check for uppercase
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    # Check for lowercase
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    # Check for digit
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"