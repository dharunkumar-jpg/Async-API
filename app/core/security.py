from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt
from pwdlib import PasswordHash
from app.core.config import get_settings
from app.exceptions.custom_exceptions import InvalidTokenException

settings = get_settings()

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Generate a secure hash for the given password.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str,hashed_password: str,) -> bool:
    """
    Verify a plain password against its hashed version.
    """
    return password_hash.verify(
        plain_password,
        hashed_password,
    )
def create_access_token(data: dict[str, Any],) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

def decode_access_token(token: str,) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    """
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

    except JWTError as exc:
        raise InvalidTokenException() from exc

