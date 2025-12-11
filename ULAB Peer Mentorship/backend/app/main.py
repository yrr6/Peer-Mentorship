
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, posts, chat

app = FastAPI(title="ULAB Peer Mentorship")

# Enable CORS so frontend can connect
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "ULAB Peer Mentorship Backend is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
