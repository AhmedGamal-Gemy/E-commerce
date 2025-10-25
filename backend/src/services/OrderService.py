from services.BaseService import BaseService
from models.models.OrderModel import OrderModel
from models.schemas.order import Order
from fastapi import HTTPException
from fastapi.requests import Request
from typing import List
from api.schemas.RequestSchemas import OrderItemRequest
from api.schemas.PaymobResponseSchema import PaymentIntentionResponse
from pydantic import EmailStr
from typing import Optional, Any
from utils.paymob import PaymobClient
from core.logging import get_logger


logger = get_logger(__name__)
class OrderService(BaseService):
    
    def __init__(self, request : Request):
        super().__init__()
        self.model = OrderModel(request)
        self.paymob = PaymobClient()

    async def checkout(self, user_details : dict, order_items:List[OrderItemRequest]) -> dict[str, Any]:
        # 1️⃣ Calculate total
        total_amount = await self.model.calculate_total(order_items)

        if total_amount <= 0:
            raise HTTPException(status_code=400, detail="Invalid order total")
        
        order_items_ids = [
            order_item.product_id
            for order_item in order_items
        ]
        # 2️⃣ Create local order (pending)
        order = Order(
            order_user_id = user_details['user_id'],
            order_items_ids = order_items_ids,
            order_total_amount = total_amount,
            order_status = "pending"
        )
        
        created_order = await self.model.create_order(order)
        if created_order is None:
            raise ValueError("Failed to create order")
        
        # 3️⃣ Create Paymob Intention
        failure_reasons : dict = {}
        paymob_response : PaymentIntentionResponse

        try:
            paymob_response = await self.paymob.create_intention(
                amount=total_amount,
                order_id = created_order.order_id,
                order_items=order_items,
                email=user_details['user_email'],
                first_name = user_details['user_first_name'],
                last_name = user_details['user_last_name'],
                address = user_details['user_address'],
                phone_number= user_details['user_phone']
            )

            client_secret = paymob_response.client_secret

            # 4️⃣ Build checkout URL
            checkout_url = f"https://accept.paymob.com/unifiedcheckout/?publicKey={self.paymob.PUBLIC_KEY}&clientSecret={client_secret}"
            status = "pending"

            # 5️⃣ Update the database ( increase sales and decrease stock )
            
            for order_item in order_items:
                is_update_success = await self.model.update_product_stock_sales(order_item["product_id"], order_item["quantity"])
                if not is_update_success:
                    logger.error(f"Product with id: {order_item["product_id"]} failed to update in the database")

        except Exception as e:
            logger.exception(e)
            checkout_url = ""
            status = "failed"
            failure_reasons = {"reasons":str(e)}

        # 5️⃣ Return structured response
        return {
            "order_id": created_order.order_id,
            "checkout_url": checkout_url,
            "total_amount": total_amount,
            "status": status,
            "created_at": created_order.order_created_at,
            "failure_reasons" : failure_reasons
        }
