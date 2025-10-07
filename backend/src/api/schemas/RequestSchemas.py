from pydantic import BaseModel
from configs.enums import UserRole
from typing import Optional

class LoginRequest(BaseModel):
    user_email : str
    user_password : str

class RegisterRequest(BaseModel):
    user_name : str
    user_email : str
    user_password : str
    user_role : Optional[UserRole] = UserRole.USER
