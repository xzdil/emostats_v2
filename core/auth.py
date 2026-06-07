# core/auth.py

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
import hmac

from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_access_token
from repositories.user import UserRepository

api_key_header = APIKeyHeader(name="X-API-Token", auto_error=False)
bearer_scheme = HTTPBearer()  # <-- Add this

from .variables import API_TOKEN

def get_api_token(api_key: str = Depends(api_key_header)):
    if api_key is None:
        raise HTTPException(status_code=401, detail="Invalid or missing API token")
    if not hmac.compare_digest(api_key, API_TOKEN):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API token")
    return api_key


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # <-- Changed
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # <-- Extract token directly
    print(f"Received token: {token}")  # <-- Debug print
    payload = decode_access_token(token)
    print(f"Decoded token payload: {payload}")  # <-- Debug print
    if not payload:
        raise HTTPException(401, "Invalid token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(401, "Invalid token payload")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(401, "User not found")

    return user


def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin only")
    return user