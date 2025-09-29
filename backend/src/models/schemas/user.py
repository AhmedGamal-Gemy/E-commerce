from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone

from configs.enums import UserRole

class User(BaseModel):
    user_id : ObjectId
    user_name : str
    user_email : str
    user_password_hash : str
    user_role : UserRole
    user_created_at : datetime = Field( default= datetime.now(timezone.utc) )

