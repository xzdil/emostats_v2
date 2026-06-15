from pydantic import field_validator
from .base import *

class UserCreate(BaseValidateModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: str

    @field_validator('email')
    def validate_email(cls, value):
        if value is not None and '@' not in value:
            raise ValueError("Invalid email address")
        return value

class UserDB(UserCreate):
    id: int
    role: str

class UserUpdate(BaseValidateModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    @field_validator('email')
    def validate_email(cls, value):
        if value is not None and '@' not in value:
            raise ValueError("Invalid email address")
        return value

class UserResponse(BaseValidateModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role: str