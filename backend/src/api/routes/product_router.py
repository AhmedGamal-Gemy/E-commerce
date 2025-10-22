from fastapi import Request, APIRouter, Query
from api.controllers.ProductController import ProductController
from api.routes.base_router import BaseRouter
from api.schemas.RequestSchemas import InsertProductRequest, UpdateProductRequest, DeleteProductRequest, GetAllProductsRequest, GetProductRequest, GetProductsByCategoryRequest, SearchProductsByNameRequest
from models.schemas.product import Product
from typing import Optional

class ProductRouter(BaseRouter):
    def __init__(self):
        super().__init__()
        self.product_router = APIRouter(
            prefix=self.settings.API_PREFIX + "/products",
            tags=["Products"],
        )

        ########################## Public routes ##############################

        @self.product_router.get("/all_products")
        async def get_all_products(
            request: Request,
            products_number_in_page: Optional[int] = Query(10, ge=1, le=100, description="Number of products per page"),
            last_seen_id: Optional[str] = Query(None, description="Last product ObjectId for keyset pagination"),
            ):
            controller = ProductController(request)
            body = GetAllProductsRequest(
                products_number_in_page = products_number_in_page,
                last_seen_id = last_seen_id
            )
            return await controller.get_all_products(body)

        @self.product_router.get("/product_by_id")
        async def get_product_by_id(
            product_id: str, 
            request: Request
            ):
            controller = ProductController(request)
            body = GetProductRequest(product_id = product_id)
            return await controller.get_product_by_id(body)

        @self.product_router.get("/search")
        async def search_products_by_query(
            request: Request,
            query: str,
            products_number_in_page: Optional[int] = Query(10, ge=1, le=100, description="Number of products per page"),
            last_seen_id: Optional[str] = Query(None, description="Last product ObjectId for keyset pagination"),
            ):
            controller = ProductController(request)
            body = SearchProductsByNameRequest(
                query = query,
                products_number_in_page = products_number_in_page,
                last_seen_id = last_seen_id
            )
            return await controller.search_products_by_query(body)

        @self.product_router.get("/category")
        async def get_products_by_category(
            request: Request,
            category_name: str = Query(..., description="Category name to filter by"),
            products_number_in_page: Optional[int] = Query(10, ge=1, le=100, description="Number of products per page"),
            last_seen_id: Optional[str] = Query(None, description="Last product ObjectId for keyset pagination"),
        ):
            controller = ProductController(request)

            body = GetProductsByCategoryRequest(
                category_name = category_name,
                products_request = GetAllProductsRequest(
                    products_number_in_page= products_number_in_page,
                    last_seen_id = last_seen_id
                )
            )
            return await controller.get_products_by_category(body)

        # @self.product_router.post("/checkout")
        # async def checkout(
        #     body: CheckoutOrderRequest,
        #     request: Request
        # ):
        #     pass

        ########################## Admin routes ##############################
        
        @self.product_router.post("/add_product")
        async def add_product(
            request: Request, 
            body : InsertProductRequest
            ):
            controller = ProductController(request)
            return await controller.add_product(body)

        @self.product_router.put("/update_product")
        async def update_product(
            request: Request, 
            body : UpdateProductRequest
            ):
            controller = ProductController(request)
            return await controller.update_product(body)
        
        @self.product_router.delete("/delete_product")
        async def delete_product(
            body: DeleteProductRequest, 
            request: Request
            ):
            controller = ProductController(request)
            return await controller.delete_product(body)

        @self.product_router.get("/basic_analysis")
        async def basic_analysis(
            request: Request
            ):
            controller = ProductController(request)
            return await controller.get_basic_analysis()

    def get_product_router(self):
        return self.product_router