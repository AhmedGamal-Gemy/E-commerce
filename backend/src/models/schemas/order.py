from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from typing import List, Optional

class Order(BaseModel):
    order_id : Optional[str] = None
    order_user_id : Optional[str] = None
    order_items_ids : List[str]
    order_total_amount : float
    order_status : Optional[str] = None
    order_created_at : datetime = Field( default= datetime.now(timezone.utc) )

