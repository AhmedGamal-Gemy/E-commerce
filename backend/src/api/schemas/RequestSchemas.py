from pydantic import BaseModel, EmailStr
from configs.enums import UserRole
from typing import Optional
from models.schemas.product import Product
from typing import List


class LoginRequest(BaseModel):
    user_email : str
    user_password : str

class RegisterRequest(BaseModel):
    user_name : str
    user_email : str
    user_password : str
    user_role : Optional[UserRole] = UserRole.USER

class InsertProductRequest(BaseModel):
    product_name : str
    product_description : str
    product_price : float
    product_category_name : str
    product_stock_quantity : int
    product_image_path : str

class UpdateProductRequest(BaseModel):
    product_id : str
    new_product : Product

class DeleteProductRequest(BaseModel):
    product_id_to_delete : str


class GetAllProductsRequest(BaseModel):
    products_number_in_page : int = 10
    last_seen_id: Optional[str] = None

class GetProductRequest(BaseModel):
    product_id : str

class GetProductsByCategoryRequest(BaseModel):
    products_request : GetAllProductsRequest
    category_name: str

class SearchProductsByNameRequest(BaseModel):
    query: str
    products_number_in_page: int
    last_seen_id: Optional[str] = None
    
class OrderItemRequest(BaseModel):
    product_id: str
    product_price: float
    quantity: int



class CheckoutOrderRequest(BaseModel):
    order_items: List[OrderItemRequest]  # what user wants to buy
    user_email: EmailStr                 # user info needed for checkout
    user_id: Optional[str] = None        # User id if he is logged in
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_address: Optional[str] = None
    user_phone: Optional[str] = None
