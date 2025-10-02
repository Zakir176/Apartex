from pydantic import BaseModel

class Token(BaseModel):
    """Access token response returned by authentication endpoints."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Decoded token data used internally for auth context."""
    email: Optional[str] = None