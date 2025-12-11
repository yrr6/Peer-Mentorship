# backend/app/services/chat_service.py

from app.models.chat import ChatMessageCreate, ChatMessage
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME
from typing import List
from datetime import datetime

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# ------------------ Save Chat Message ------------------ #
async def save_message(message_data: ChatMessageCreate) -> ChatMessage:
    """
    Save a chat message to MongoDB
    """
    message_dict = message_data.dict()
    message_dict["timestamp"] = datetime.utcnow()
    result = await db.chat.insert_one(message_dict)
    saved_message = await db.chat.find_one({"_id": result.inserted_id})
    return ChatMessage(**saved_message)

# ------------------ Get Recent Messages ------------------ #
async def get_recent_messages(limit: int = 50) -> List[ChatMessage]:
    """
    Retrieve recent chat messages from MongoDB
    """
    messages_cursor = db.chat.find().sort("timestamp", -1).limit(limit)
    messages_list = await messages_cursor.to_list(length=limit)
    return [ChatMessage(**msg) for msg in reversed(messages_list)]
