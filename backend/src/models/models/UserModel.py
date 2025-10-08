from models.models.BaseModel import BaseModel
from models.schemas.user import User
from configs.enums import CollectionNames
from datetime import datetime, timezone, timedelta
from pydantic import EmailStr
from fastapi import Request
import hashlib, hmac
from bson import ObjectId
from typing import Optional

class UserModel(BaseModel):

    def __init__(self, request : Request):

        super().__init__( request = request, collection_name= CollectionNames.USERS )

        self.logger.info(f"UserModel initialized")

    async def create_user(self, user: User) -> Optional[User]:

        user_data = user.model_dump( mode = "json" )
        user_data["user_created_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(user_data)

        if result.inserted_id:
            created_user = await self.collection.find_one({"_id": result.inserted_id})
            return created_user
        else:
            self.logger.error("Failed to insert user.")
            return None

    async def get_user_by_email(self, email : EmailStr):

        resulted_user = await self.collection.find_one({"user_email" : email})

        if resulted_user:
            return resulted_user
        return None
    
    async def store_refresh_token(self, user_id : str, refresh_token : str) -> bool:

        refresh_secret = self.settings.REFRESH_TOKEN_SECRET.encode()

        hashed_token = hmac.new(
            key = refresh_secret, 
            msg = refresh_token.encode(), 
            digestmod = hashlib.sha256 
            ).hexdigest()
        
        now_date = datetime.now(timezone.utc)

        result = await self.collection.update_one(
            {"_id" : ObjectId(user_id)},
            {"$set" : {
                "refresh_token" : hashed_token,
                "refresh_token_created_at" : now_date,
                "refresh_token_expires_at": now_date + timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)
                }}
        )

        return result.modified_count > 0
