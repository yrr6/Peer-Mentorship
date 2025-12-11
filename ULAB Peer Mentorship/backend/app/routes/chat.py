from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.chat import ChatMessage, ChatMessageCreate
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME
import json
from typing import List

router = APIRouter()

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# In-memory connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ------------------ WebSocket Endpoint ------------------ #
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Save chat message to MongoDB
            msg_dict = json.loads(data)
            chat_msg = ChatMessageCreate(**msg_dict)
            await db.chat.insert_one(chat_msg.dict())

            # Broadcast to all connected clients
            await manager.broadcast(f"{chat_msg.sender_name}: {chat_msg.message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
