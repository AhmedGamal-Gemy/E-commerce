from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone

class Auth(BaseModel):
    auth_user_id : ObjectId
    auth_refresh_token : str
    auth_token_expiry : datetime
    auth_session_created_at : datetime = Field( default= datetime.now(timezone.utc) )

