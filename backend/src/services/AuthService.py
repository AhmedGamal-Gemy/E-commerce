from services.BaseService import BaseService
from models.models.UserModel import UserModel
from models.schemas.user import User
from fastapi.requests import Request

class AuthService(BaseService):
    
    def __init__(self, request : Request):
        super().__init__()
        self.model = UserModel(request)

    async def register(self, user : User) -> dict:
        
        user = await self.model.create_user( user = user )
        return user


