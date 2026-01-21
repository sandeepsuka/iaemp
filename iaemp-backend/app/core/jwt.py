import os
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    # 🔑 REQUIRED FOR AUTH
    if "sub" not in to_encode:
        raise ValueError("JWT must include 'sub'")

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

