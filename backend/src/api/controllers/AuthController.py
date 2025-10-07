from api.controllers.BaseController import BaseController
from api.schemas.RequestSchemas import LoginRequest, RegisterRequest
from api.schemas.ResponseSchemas import AuthResponse, UserResponse, RegisterResult
from services.AuthService import AuthService
from models.schemas.user import User
from fastapi.requests import Request
from passlib.hash import bcrypt


class AuthController(BaseController):

    def __init__(self, request : Request) -> None:
        super().__init__()
        self.auth_service = AuthService(request = request)

    async def login(self, request : LoginRequest) -> AuthResponse:
        pass

    async def register(self, request : RegisterRequest) -> RegisterResult:

        user_password_hash = bcrypt.hash(request.user_password)

        user = User(
            user_name = request.user_name,
            user_email = request.user_email,
            user_password_hash = user_password_hash,
            user_role = request.user_role
        )

        created_user = await self.auth_service.register(user = user)

        return RegisterResult(
            user = created_user,
            access_token = "None"
        )