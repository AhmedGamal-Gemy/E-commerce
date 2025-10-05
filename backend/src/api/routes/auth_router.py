from fastapi import APIRouter, Depends
from api.routes.base_router import BaseRouter

from api.routes.schemas.RequestSchemas import LoginRequest, RegisterRequest
from api.routes.schemas.ResponseSchemas import AuthResponse

from api.controllers.AuthController import AuthController

from fastapi.requests import Request

class AuthRouter(BaseRouter):

    def __init__(self):

        self
        super().__init__()
        self.auth_router = APIRouter(
            prefix = self.settings.API_PREFIX + "/auth",
            tags=["Authentication"],
        )



        @self.auth_router.post("/login", response_model = AuthResponse)
        async def login(
            body : LoginRequest,
            request : Request,
            ):

            auth_controller = AuthController(request=request)
            response = await auth_controller.login(body)
            return response



        @self.auth_router.post("/register", response_model = AuthResponse)
        async def register( 
            body : RegisterRequest,
            request : Request
            ):

            auth_controller = AuthController(request=request)
            response = await auth_controller.register(body)
            return response            
        
        
    def get_auth_router(self) -> APIRouter :
        return self.auth_router
