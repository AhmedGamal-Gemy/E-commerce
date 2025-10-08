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
    refresh_token: Optional[str] = None

class RegisterResult(NamedTuple):
    user : User
    access_token : Optional[str]


class InsertProductResponse(BaseModel):
    product_id : str
    product_name : str
    product_description : str
    product_price : float
    product_category_name : str
    product_stock_quantity : int
