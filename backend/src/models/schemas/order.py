from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from typing import List
from src.models.schemas.order_item import OrderItem

class Order(BaseModel):
    order_id : ObjectId
    order_user_id : ObjectId
    order_items : List[OrderItem]
    order_total_amount : float
    order_status : str
    order_created_at : datetime = Field( default= datetime.now(timezone.utc) )

