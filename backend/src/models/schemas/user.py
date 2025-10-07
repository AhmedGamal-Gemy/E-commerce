from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import datetime, timezone

from configs.enums import UserRole

class User(BaseModel):
    user_name : str
    user_email : EmailStr
    user_password_hash : str
    user_role : UserRole = UserRole.USER
    
    user_created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

