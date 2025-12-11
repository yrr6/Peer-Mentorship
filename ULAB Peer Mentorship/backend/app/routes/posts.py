from fastapi import APIRouter, HTTPException, Depends, Header
from app.models.post import Post, PostCreate
from app.config import MONGO_URI, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import jwt
from app.config import JWT_SECRET

router = APIRouter()

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# ------------------ Helper: Verify JWT ------------------ #
async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ------------------ Create Post ------------------ #
@router.post("/create")
async def create_post(post: PostCreate, user=Depends(get_current_user)):
    post_dict = {
        "user_id": user["user_id"],
        "user_name": user["email"],
        "text": post.text,
        "approved": False  # Admin approval required
    }
    result = await db.posts.insert_one(post_dict)
    return {"message": "Post created", "post_id": str(result.inserted_id)}

# ------------------ Get All Approved Posts ------------------ #
@router.get("/all", response_model=List[Post])
async def get_all_posts():
    posts_cursor = db.posts.find({"approved": True}).sort("created_at", -1)
    posts = await posts_cursor.to_list(length=100)
    return posts

# ------------------ Admin: Get Pending Posts ------------------ #
@router.get("/pending", response_model=List[Post])
async def get_pending_posts(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    posts_cursor = db.posts.find({"approved": False}).sort("created_at", -1)
    posts = await posts_cursor.to_list(length=100)
    return posts

# ------------------ Admin: Approve Post ------------------ #
@router.post("/approve/{post_id}")
async def approve_post(post_id: str, user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.posts.update_one({"_id": post_id}, {"$set": {"approved": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post approved"}
