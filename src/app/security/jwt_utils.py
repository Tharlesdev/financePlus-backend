import os
import jwt
from datetime import datetime, timedelta, timezone


def create_token(user_id: str):
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")

    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")


def verify_token(token: str):
    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY is not set in environment variables")

    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded["sub"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
