from fastapi import Request, APIRouter
from api.controllers.ProductController import ProductController
from api.routes.base_router import BaseRouter
from api.schemas.RequestSchemas import InsertProductRequest


class ProductRouter(BaseRouter):
    def __init__(self):
        super().__init__()
        self.product_router = APIRouter(
            prefix=self.settings.API_PREFIX + "/products",
            tags=["Products"],
        )

        ########################## Public routes ##############################

        @self.product_router.get("/all_products")
        async def get_all_products(request: Request):
            controller = ProductController(request)
            return await controller.get_all_products()

        @self.product_router.get("/product_by_id/{product_id}")
        async def get_product_by_id(product_id: str, request: Request):
            controller = ProductController(request)
            return await controller.get_product_by_id(product_id)

        @self.product_router.get("/search")
        async def search_products_by_name(query: str, request: Request):
            controller = ProductController(request)
            return await controller.search_products_by_name(query)

        @self.product_router.get("/category/{category_name}")
        async def get_products_by_category(category_name: str, request: Request):
            controller = ProductController(request)
            return await controller.get_products_by_category(category_name)

        ########################## Admin routes ##############################
        
        @self.product_router.post("/add_product")
        async def add_product(
            request: Request, 
            body : InsertProductRequest
            ):
            controller = ProductController(request)
            return await controller.add_product(body)

        @self.product_router.put("/update_product/{product_id}")
        async def update_product(product_id: str, request: Request):
            controller = ProductController(request)
            return await controller.update_product(product_id)

        @self.product_router.delete("/delete_product/{product_id}")
        async def delete_product(product_id: str, request: Request):
            controller = ProductController(request)
            return await controller.delete_product(product_id)

    def get_product_router(self):
        return self.product_router