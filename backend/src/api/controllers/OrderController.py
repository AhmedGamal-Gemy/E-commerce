from api.controllers.BaseController import BaseController
from fastapi.requests import Request
from services.OrderService import OrderService
from api.schemas.RequestSchemas import CheckoutOrderRequest
from api.schemas.ResponseSchemas import CheckoutOrderResponse
from datetime import datetime, timezone
from core.logging import get_logger


logger = get_logger(__name__)
class OrderController(BaseController):

    def __init__(self, request : Request) -> None:
        super().__init__()
        self.order_service = OrderService(request = request)


    async def checkout(self, body : CheckoutOrderRequest)-> CheckoutOrderResponse:
        
        try:
            order_items = body.order_items 
            user_email = body.user_email
            user_id = body.user_id
            user_first_name = body.user_first_name
            user_last_name = body.user_last_name
            user_address = body.user_address
            user_phone = body.user_phone

            user_details = {
                "user_id" : user_id,
                "user_first_name": user_first_name,
                "user_email" : user_email,
                "user_last_name": user_last_name,
                "user_address": user_address,
                "user_phone" : user_phone
            }

            response = await self.order_service.checkout(order_items = order_items, user_details = user_details)

            return CheckoutOrderResponse(
                **response
            )
        except Exception as e:

            logger.exception(e)
            
            return CheckoutOrderResponse(
                order_id = "",
                checkout_url = "",
                total_amount = 0.0,
                status = "failed",
                created_at = datetime.now(timezone.utc),
                failure_reasons = {"reasons" : str(e)}
            )