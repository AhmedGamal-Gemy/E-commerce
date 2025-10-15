from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional

class Product(BaseModel):
    product_id : Optional[str] = None
    product_name : str
    product_description : str
    product_price : float
    product_created_at : datetime = Field( default= datetime.now(timezone.utc) )
    product_category_name : str
    product_stock_quantity : int
    product_image_path : str
    product_sales: int = 0
