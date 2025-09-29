from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone

class OrderItem(BaseModel):
    order_item_id : ObjectId
    order_item_order_id : ObjectId
    order_item_product_id : ObjectId
    order_item_quantity : int
    order_item_price : float

