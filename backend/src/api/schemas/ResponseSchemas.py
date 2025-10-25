from pydantic import BaseModel, EmailStr
from configs.enums import UserRole
from typing import Optional, NamedTuple, List
from models.schemas.user import User
from models.schemas.product import Product
from datetime import datetime

class UserResponse(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    user_role: UserRole

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: Optional[str] = None

class RegisterResult(NamedTuple):
    user : User
    access_token : Optional[str]


class InsertProductResponse(BaseModel):
    product_id : str
    product_name : str
    product_description : str
    product_price : float
    product_category_name : str
    product_stock_quantity : int

class UpdateProductResponse(BaseModel):
    updated_product : Product
    did_upsert : bool

class DeleteProductResponse(BaseModel):
    is_delete_success : bool


class GetAllProductsResponse(BaseModel):
    products: List[Product]
    total_pages: int
    last_seen_id: Optional[str] = None
    current_page: int

class GetProductResponse(BaseModel):
    product: Optional[Product]

class GetBasicAnalysisResponse(BaseModel):
    numOfProductsInTheStock : int
    numOfSaledProducts : int
    totalPriceOfAllProductsInTheStock : int 
    totalPriceOfSaledProducts : int 
    theMostSaledProduct : Optional[Product]

class CheckoutOrderResponse(BaseModel):
    order_id: str
    checkout_url: str
    total_amount: float
    status: str = "pending"
    created_at: datetime
    failure_reasons : dict

 