from pydantic import BaseModel, EmailStr
from configs.enums import UserRole
from typing import Optional

class UserResponse(BaseModel):
    id: str
    user_name: str
    user_email: EmailStr
    user_role: UserRole

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str

