from app.models.post import PostCreate, Post
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME
from typing import List
from datetime import datetime
from bson import ObjectId

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# ------------------ Create Post ------------------ #
async def create_post(user_id: str, user_name: str, post_data: PostCreate) -> Post:
    
    post_dict = {
        "user_id": user_id,
        "user_name": user_name,
        "text": post_data.text,
        "created_at": datetime.utcnow(),
        "approved": False
    }
    result = await db.posts.insert_one(post_dict)
    saved_post = await db.posts.find_one({"_id": result.inserted_id})
    return Post(**saved_post)

# ------------------ Get All Approved Posts ------------------ #
async def get_all_posts(limit: int = 100) -> List[Post]:
    cursor = db.posts.find({"approved": True}).sort("created_at", -1).limit(limit)
    posts_list = await cursor.to_list(length=limit)
    return [Post(**post) for post in posts_list]

# ------------------ Get Pending Posts for Admin ------------------ #
async def get_pending_posts(limit: int = 100) -> List[Post]:
    cursor = db.posts.find({"approved": False}).sort("created_at", -1).limit(limit)
    posts_list = await cursor.to_list(length=limit)
    return [Post(**post) for post in posts_list]

# ------------------ Approve a Post ------------------ #
async def approve_post(post_id: str) -> bool:
    result = await db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {"approved": True}})
    return result.modified_count > 0
