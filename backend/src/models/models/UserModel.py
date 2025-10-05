from models.models.BaseModel import BaseModel
from models.schemas.user import User
from configs.enums import CollectionNames
from datetime import datetime, timezone

from fastapi import Request
class UserModel(BaseModel):

    def __init__(self, request : Request):

        super().__init__( request = request, collection_name= CollectionNames.USERS )

        self.logger.info(f"UserModel initialized")

    async def create_user(self, user: User) -> dict:

        user_data = user.model_dump( mode = "json" )
        user_data["user_created_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(user_data)

        if result.inserted_id:
            created_user = await self.collection.find_one({"_id": result.inserted_id})
            
            # ✅ Transform Mongo document -> Pydantic-compatible
            created_user["user_id"] = str(created_user["_id"])
            created_user.pop("_id", None)
            
            created_user.pop("user_password_hash", None)
            return created_user
        else:
            self.logger.error("Failed to insert user.")
            return None

