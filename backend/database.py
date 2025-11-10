import os
from datetime import datetime
from typing import Any, Dict, Optional, List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

# expose a shared db instance for simple usage with FastAPI lifespan
import asyncio
loop = asyncio.get_event_loop()
_db_sync = None
try:
    _client_sync = AsyncIOMotorClient(DATABASE_URL)
    _db_sync = _client_sync[DATABASE_NAME]
except Exception:
    _db_sync = None

async def db():
    # backward compatible attribute used in main
    return await get_db()

# helpers matching instructions
async def create_document(collection_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    database = _db_sync or await get_db()
    now = datetime.utcnow()
    payload = {**data, "created_at": now, "updated_at": now}
    result = await database[collection_name].insert_one(payload)
    if result.inserted_id:
        return {"_id": str(result.inserted_id), **data}
    return None

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    database = _db_sync or await get_db()
    cursor = database[collection_name].find(filter_dict or {}).limit(limit)
    docs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # stringify ObjectId
        docs.append(doc)
    return docs
