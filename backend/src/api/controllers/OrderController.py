from api.controllers.BaseController import BaseController
from fastapi.requests import Request
from services.OrderService import OrderService
from api.schemas.RequestSchemas import CheckoutOrderRequest
from api.schemas.ResponseSchemas import CheckoutOrderResponse

class OrderController(BaseController):

    def __init__(self, request : Request) -> None:
        super().__init__()
        self.auth_service = OrderService(request = request)


    async def checkout(self, body : CheckoutOrderRequest)-> CheckoutOrderResponse:
        pass