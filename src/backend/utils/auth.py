from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from backend.configs.config import settings

security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    """
    Decodes and verifies the Supabase JWT.
    Returns the payload (claims) if valid.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )