from pydantic import BaseModel


class Token(BaseModel):
    """
    Response returned after successful authentication.
    """

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    Data stored inside the JWT token.
    """

    sub: str