from pydantic import BaseModel
from configs.enums import UserRole
from typing import Optional

class LoginRequest(BaseModel):
    user_email : str
    user_password : str

class RegisterRequest(BaseModel):
    user_name : str
    user_email : str
    user_password : str
    user_role : Optional[UserRole] = UserRole.USER

class AllProductsRequest(BaseModel):
    page_number : int
    products_number_in_page : int = 10

class InsertProductRequest(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    product_category_name : str
    product_stock_quantity : int
    product_image_path : str