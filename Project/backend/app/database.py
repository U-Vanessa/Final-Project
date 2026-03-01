from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            self.database = self.client[settings.DATABASE_NAME]
            logger.info("Connected to MongoDB successfully!")
            
            # Create indexes
            await self.create_indexes()
            return self.database
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def create_indexes(self):
        """Create database indexes for better performance"""
        # User collection indexes
        await self.database.users.create_index("email", unique=True)
        await self.database.users.create_index("username", unique=True)
        
        # Members collection indexes
        await self.database.members.create_index("email", unique=True)
        await self.database.members.create_index("user_id")
        
        # Reports collection indexes
        await self.database.reports.create_index("user_id")
        await self.database.reports.create_index([("created_at", -1)])
        
        logger.info("Database indexes created successfully")

db = Database()

async def get_database():
    """Dependency to get database instance"""
    if db.database is None:
        await db.connect()
    return db.database