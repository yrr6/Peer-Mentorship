import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/peer_mentorship")

# Database name
DB_NAME = os.getenv("DB_NAME", "peer_mentorship")

# JWT secret key
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")

# JWT algorithm
JWT_ALGORITHM = "HS256"

# Token expiration in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 60
