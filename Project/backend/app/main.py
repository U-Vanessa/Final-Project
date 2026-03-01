# app/main.py - UPDATED VERSION WITH AUTH
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()

# Try to import database and auth, but handle if they don't exist yet
try:
    from app.database import db
    DATABASE_AVAILABLE = True
except ImportError:
    logger.warning("Database module not available")
    DATABASE_AVAILABLE = False
    db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting RAB Dashboard API...")
    
    if DATABASE_AVAILABLE and db:
        try:
            await db.connect()
            logger.info("✅ MongoDB connected successfully!")
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
    else:
        logger.warning("⚠️ Database not configured")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")
    if DATABASE_AVAILABLE and db:
        await db.disconnect()

# Create FastAPI app
app = FastAPI(
    title="RAB Dashboard API",
    description="Backend API for RAB Dashboard with Authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
# In your main.py, update CORS if needed:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
        # Add your frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router - THIS IS WHAT'S MISSING!
try:
    from app.api.auth import router as auth_router
    app.include_router(auth_router)
    logger.info("✅ Auth routes loaded successfully!")
except ImportError as e:
    logger.error(f"❌ Failed to load auth routes: {e}")
    # Print detailed error for debugging
    import traceback
    logger.error(traceback.format_exc())

# Create a temporary auth router for testing
    from fastapi import APIRouter
    auth_router = APIRouter(prefix="/auth", tags=["authentication"])
    
    @auth_router.get("/test")
    async def auth_test():
        return {"message": "Auth module is working!"}
    
    @auth_router.post("/login")
    async def login_test():
        return {"message": "Login endpoint placeholder"}
    
    app.include_router(auth_router)
    logger.warning("⚠️ Using temporary auth routes")