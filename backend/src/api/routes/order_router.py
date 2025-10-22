from fastapi import APIRouter, Depends
from api.routes.base_router import BaseRouter
from fastapi.requests import Request

class OrderRouter(BaseRouter):

    def __init__(self):

        super().__init__()
        self.order_router = APIRouter(
            prefix = self.settings.API_PREFIX + "/orders",
            tags=["Orders"],
        )

        @self.order_router.get("/test")
        async def test_order():
            return "order router is working"       
        
        # @self.order_router.post("/checkout")
        # async def checkout(
        #     request : Request,
        #     body : 
        # )-> :
        #     pass
        
    def get_order_router(self) -> APIRouter:
        return self.order_router
