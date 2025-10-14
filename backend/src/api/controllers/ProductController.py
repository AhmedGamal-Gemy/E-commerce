from api.controllers.BaseController import BaseController
from services.ProductService import ProductService
from fastapi import Request
from api.schemas.RequestSchemas import InsertProductRequest, UpdateProductRequest, DeleteProductRequest, GetAllProductsRequest
from api.schemas.ResponseSchemas import InsertProductResponse, UpdateProductResponse, DeleteProductResponse, GetAllProductsResponse
from models.schemas.product import Product
from datetime import datetime, timezone

class ProductController(BaseController):
    
    def __init__(self, request : Request):
        super().__init__()
        self.product_service = ProductService( request = request )

    ################## NORMAL PAGES ##########################

    async def get_all_products(self, body: GetAllProductsRequest) -> GetAllProductsResponse:
        current_page = GetAllProductsRequest.current_page
        products_number_in_page = GetAllProductsRequest.products_number_in_page
        last_seen_id = GetAllProductsRequest.last_seen_id

        products, total_pages  = await self.product_service.get_all_products( 
            current_page = current_page, 
            products_number_in_page = products_number_in_page,
            last_seen_id = last_seen_id
        )             

        return GetAllProductsResponse(
            products = products,
            total_pages = total_pages,
            last_seen_id = last_seen_id
        )


    async def get_product_by_id(self, product_id):
        pass

    async def search_products_by_name(self, query):
        pass 

    async def get_products_by_category(self, category_name):
        pass

    ################## ADMIN DASHBOARD ##########################

    async def add_product(self, product_request : InsertProductRequest) -> InsertProductResponse:
        
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

        return InsertProductResponse(**inserted_product)


    async def update_product(self, body : UpdateProductRequest) -> UpdateProductResponse:
        
        product_id = body.product_id
        new_product_to_update = body.new_product

        updated_product, did_upsert = await self.product_service.update_product( product_id = product_id, new_product = new_product_to_update )

        return UpdateProductResponse(
            updated_product = Product(**updated_product), 
            did_upsert = did_upsert
            )

        
    async def delete_product(self, body : DeleteProductRequest) -> DeleteProductResponse:
        
        product_id_to_delete = body.product_id_to_delete

        is_delete_success = await self.product_service.delete_product( product_id_to_delete = product_id_to_delete )

        return DeleteProductResponse(
            is_delete_success = is_delete_success
        )