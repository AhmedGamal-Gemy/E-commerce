from configs.settings import get_settings
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt

settings = get_settings()

def create_access_token(data : dict, expires_delta : Optional[timedelta] = None) -> str:
    
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims = to_encode, 
        key = settings.JWT_SECRET_KEY, 
        algorithm = settings.JWT_ALGORITHM
        )
    
    return encoded_jwt


def create_refresh_token(data : dict) -> str:
    
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) +  timedelta(days= settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(
        claims = to_encode, 
        key = settings.JWT_SECRET_KEY, 
        algorithm = settings.JWT_ALGORITHM
        )
    
    return encoded_jwt
