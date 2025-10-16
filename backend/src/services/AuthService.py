from services.BaseService import BaseService
from models.models.UserModel import UserModel
from models.schemas.user import User
from fastapi.requests import Request
from typing import Optional, Tuple
from fastapi import HTTPException, status
from utils.jwt_utils import create_access_token, create_refresh_token
from api.schemas.RequestSchemas import LoginRequest
from api.schemas.ResponseSchemas import AuthResponse
from passlib.hash import bcrypt


class AuthService(BaseService):
    
    def __init__(self, request : Request):
        super().__init__()
        self.model = UserModel(request)

    async def check_user_exists(self, user : User) -> Optional[dict]:
        resulted_user = await self.model.get_user_by_email(user.user_email)
        return resulted_user

    async def register(self, user : User) -> Tuple[Optional[User],Optional[str], Optional[str]]:
        
        existing_user = await self.check_user_exists(user)

        # Check if user exists on database by the email
        if existing_user:

            # Raise FastAPI HTTPException 
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "User with this email already exists"
            )


        new_user = await self.model.create_user( user = user )

        if not new_user:
            raise HTTPException(status_code=500, detail="User registration failed.")
        
        # JWT access and refresh tokens
        payload = {
            "sub": str(new_user["_id"]),
            "user_name" : new_user["user_name"],
            "user_email": new_user["user_email"],
            "user_role": new_user["user_role"]
        }

        access_token = create_access_token( data = payload )
        refresh_token = create_refresh_token( data = payload )

        refresh_is_stored = await self.model.store_refresh_token(user_id = new_user["_id"], refresh_token = refresh_token)
        
        if refresh_is_stored:
            self.logger.info(f"Refresh token is stored successfully for the user id : {new_user["_id"]}")
        else:
            self.logger.warning(f"Refresh token is NOT stored successfully for the user id : {new_user["_id"]}")


        # ✅ Transform Mongo document -> Pydantic-compatible
        new_user["user_id"] = str(new_user["_id"])
        new_user.pop("_id", None)
        
        new_user.pop("user_password_hash", None)

        return new_user, access_token, refresh_token

    async def login(self, entered_user: LoginRequest) -> Tuple[User, str, str]:
        resulted_user = await self.model.get_user_by_email(entered_user.user_email)

        if not resulted_user or not bcrypt.verify(entered_user.user_password, resulted_user['user_password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        payload = {
            "sub": str(resulted_user["_id"]),
            "user_name": resulted_user["user_name"],
            "user_email": resulted_user["user_email"],
            "user_role": resulted_user["user_role"],
        }

        access_token = create_access_token(data=payload)
        refresh_token = create_refresh_token(data=payload)

        await self.model.store_refresh_token(user_id=resulted_user["_id"], refresh_token=refresh_token)

        resulted_user["user_id"] = str(resulted_user.pop("_id"))
        resulted_user.pop("user_password_hash", None)

        return resulted_user, access_token, refresh_token

                