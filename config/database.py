from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from typing import Any, Optional  # Add these imports
import os

load_dotenv()

class Database:
    client: Optional[Any] = None  # Use Any to bypass strict type checking
    db = None

    @classmethod
    async def connect(cls):
        cls.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        cls.db = cls.client.get_database("bank_db")

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()

db = Database()