from api.controllers.BaseController import BaseController
from services.ProductService import ProductService
from fastapi import Request
from api.schemas.RequestSchemas import InsertProductRequest, UpdateProductRequest, DeleteProductRequest, GetAllProductsRequest, GetProductRequest, GetProductsByCategoryRequest, SearchProductsByNameRequest
from api.schemas.ResponseSchemas import InsertProductResponse, UpdateProductResponse, DeleteProductResponse, GetAllProductsResponse, GetProductResponse, GetBasicAnalysisResponse
from models.schemas.product import Product
from datetime import datetime, timezone

class ProductController(BaseController):
    
    def __init__(self, request : Request):
        super().__init__()
        self.product_service = ProductService( request = request )

    ################## NORMAL PAGES ##########################

    async def get_all_products(self, body: GetAllProductsRequest) -> GetAllProductsResponse:
        products_number_in_page = body.products_number_in_page
        last_seen_id = body.last_seen_id

        paginated_products, total_pages, last_seen_id, current_page  = await self.product_service.get_all_products( 
            products_number_in_page = products_number_in_page,
            last_seen_id = last_seen_id
        )             

        products = [
            Product(**product)
            for product in paginated_products
        ]

        return GetAllProductsResponse(
            products = products,
            total_pages = total_pages,
            last_seen_id = last_seen_id,
            current_page = current_page
        )


    async def get_product_by_id(self, body: GetProductRequest) -> GetProductResponse:
        
        product_id = body.product_id
        product = await self.product_service.get_product_by_id(product_id = product_id)
        
        return GetProductResponse(product = product)

    async def search_products_by_query(self, body: SearchProductsByNameRequest) -> GetAllProductsResponse:
        query = body.query
        products_number_in_page = body.products_number_in_page
        last_seen_id = body.last_seen_id

        products_dicts, total_pages, last_seen_id, current_page = await self.product_service.search_products_by_query(
            query= query,
            products_number_in_page= products_number_in_page,
            last_seen_id= last_seen_id
        )
        
        products = [
            Product(**product)
            for product in products_dicts
        ]

        return GetAllProductsResponse(
            products = products,
            total_pages = total_pages,
            current_page = current_page,
            last_seen_id = last_seen_id
        )


    async def get_products_by_category(self, body: GetProductsByCategoryRequest) -> GetAllProductsResponse:
        category_name = body.category_name
        products_number_in_page = body.products_request.products_number_in_page
        last_seen_id = body.products_request.last_seen_id
        
        products_dicts, total_pages, last_seen_id, current_page = await self.product_service.get_products_by_category(
            category= category_name,
            products_number_in_page= products_number_in_page,
            last_seen_id= last_seen_id
        )
        
        products = [
            Product(**product)
            for product in products_dicts
        ]

        return GetAllProductsResponse(
            products = products,
            total_pages = total_pages,
            current_page = current_page,
            last_seen_id = last_seen_id
        )


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
    

    async def get_basic_analysis(self):
        basic_analysis = await self.product_service.get_basic_analysis()
        return GetBasicAnalysisResponse(
            **basic_analysis
        )