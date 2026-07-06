from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints


class UserBase(BaseModel):
    """
        Common fields shared across user schemas.
        """
    full_name: Annotated[str, StringConstraints(
        min_length=1,
        max_length=100,
        strip_whitespace=True),]

    email: EmailStr

class UserCreate(UserBase):
    password:Annotated[str, StringConstraints(
        min_length=8,
        max_length=128),]

class UserUpdate(BaseModel):
        """
            Schema used for updating user details.
            All fields are optional.
            """
        full_name: Annotated[str, StringConstraints(
            min_length=1,
            max_length=100,
            strip_whitespace=True),] | None = None

        email: EmailStr | None = None
        is_active: bool | None = None

        model_config = ConfigDict(extra="forbid",)

class UserResponse(UserBase):
    """
        Schema returned to the client.
        """
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True)

class UserLogin(BaseModel):
    """
    Schema used for user authentication.
    """
    email: EmailStr

    password: str

class ChangePassword(BaseModel):
    """
    Schema for changing a user's password.
    """

    current_password: str
    new_password: str








