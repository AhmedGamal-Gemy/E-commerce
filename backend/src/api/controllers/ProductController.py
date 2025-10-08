from api.controllers.BaseController import BaseController
from services.ProductService import ProductService
from fastapi import Request
from api.schemas.RequestSchemas import InsertProductRequest
from api.schemas.ResponseSchemas import InsertProductResponse
from models.schemas.product import Product
from datetime import datetime, timezone

class ProductController(BaseController):
    
    def __init__(self, request : Request):
        super().__init__()
        self.product_service = ProductService( request = request )

    ################## NORMAL PAGES ##########################

    async def get_all_products(self):
        pass

    async def get_product_by_id(self, product_id):
        pass

    async def search_products_by_name(self, query):
        pass 

    async def get_products_by_category(self, category_name):
        pass

    ################## ADMIN DASHBOARD ##########################

    async def add_product(self, product_request : InsertProductRequest) -> dict:
        
        product = Product(
            product_name = product_request.product_name,
            product_description = product_request.product_description,
            product_price = product_request.product_price,
            product_created_at = datetime.now(timezone.utc),
            product_category_name = product_request.product_category_name,
            product_stock_quantity = product_request.product_stock_quantity,
            product_image_path = product_request.product_image_path
        )

        inserted_product = await self.product_service.add_product(product = product)

        return inserted_product


    async def update_product(self, product_id):
        pass

    async def delete_product(self, product_id):
        pass