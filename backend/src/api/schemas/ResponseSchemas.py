from pydantic import BaseModel, EmailStr
from configs.enums import UserRole
from typing import Optional, NamedTuple
from models.schemas.user import User


class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    user_role: UserRole

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str

class RegisterResult(NamedTuple):
    user : User
    access_token : Optional[str]

