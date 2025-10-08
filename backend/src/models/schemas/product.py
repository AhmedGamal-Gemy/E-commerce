from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone

class Product(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    product_created_at : datetime = Field( default= datetime.now(timezone.utc) )
    product_category_name : str
    product_stock_quantity : int
    product_image_path : str

