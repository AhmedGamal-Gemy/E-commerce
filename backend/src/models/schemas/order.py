from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from typing import List, Optional

class Order(BaseModel):
    order_id : str
    order_items : List[str]
    order_total_amount : float
    order_status : Optional[str]
    order_created_at : datetime = Field( default= datetime.now(timezone.utc) )

