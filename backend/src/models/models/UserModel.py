from models.models.BaseModel import BaseModel
from models.schemas.user import User
from configs.enums import CollectionNames
from datetime import datetime, timezone
from pydantic import EmailStr

from fastapi import Request
class UserModel(BaseModel):

    def __init__(self, request : Request):

        super().__init__( request = request, collection_name= CollectionNames.USERS )

        self.logger.info(f"UserModel initialized")

    async def create_user(self, user: User) -> User:

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

        resulted_user = self.collection.find_one({"user_email" : email})
        return User(**resulted_user)