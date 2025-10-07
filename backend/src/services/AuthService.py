from services.BaseService import BaseService
from models.models.UserModel import UserModel
from models.schemas.user import User
from fastapi.requests import Request
from typing import Optional, Tuple
from fastapi import HTTPException, status

class AuthService(BaseService):
    
    def __init__(self, request : Request):
        super().__init__()
        self.model = UserModel(request)

    async def check_user_eixsts(self, user : User) -> bool:
        resulted_user = await self.model.get_user_by_email(user.user_email)
        if resulted_user:
            return True
        return False

    async def register(self, user : User) -> Tuple[Optional[User],Optional[str]]:
        
        existing_user = await self.check_user_eixsts(user)

        # Check if user exists on database by the email
        if existing_user:

            # Raise FastAPI HTTPException 
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "User with this email already exists"
            )


        new_user = await self.model.create_user( user = user )

        # ✅ Transform Mongo document -> Pydantic-compatible
        new_user["user_id"] = str(new_user["_id"])
        new_user.pop("_id", None)
        
        new_user.pop("user_password_hash", None)
        
        access_token = None

        return new_user, access_token



