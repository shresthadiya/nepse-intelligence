from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi.security import HTTPBearer
from pwdlib import PasswordHash
from app.core.config import settings

# Password hashing
password_hash = PasswordHash.recommended()

# Bearer token authentication
bearer_scheme = HTTPBearer()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password
    )

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
