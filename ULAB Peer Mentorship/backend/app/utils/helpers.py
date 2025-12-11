from fastapi import Header, HTTPException, Depends
import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM

# ------------------ JWT Verification ------------------ #
async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except IndexError:
        raise HTTPException(status_code=401, detail="Authorization header malformed")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ------------------ Role Verification ------------------ #
def verify_admin(user_payload: dict):
    if user_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return True
