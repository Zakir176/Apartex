from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import os
from typing import Optional  # Add this for type hints

# Config (use env vars in production)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_change_me')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt.

    Notes:
        bcrypt considers only the first 72 bytes; input is truncated to avoid
        mismatches between hashing and verification for longer inputs.
    """
    # bcrypt max is 72 bytes, truncate if necessary
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a plaintext password against a bcrypt hash.

    Returns:
        bool: True if the password matches the hash, otherwise False.
    """
    if len(password) > 72:
        password = password[:72]
    return pwd_context.verify(password, hashed)

def create_access_token(subject: str) -> str:
    """Create a signed JWT access token.

    Args:
        subject: Unique identifier (e.g., user email) to set as the token subject.

    Returns:
        str: Encoded JWT with expiration configured by ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {'sub': str(subject), 'exp': expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token.

    Returns:
        Optional[dict]: Decoded payload if valid; None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        return None