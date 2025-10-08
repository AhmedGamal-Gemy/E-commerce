from services.BaseService import BaseService
from models.models.ProductModel import ProductModel
from configs.enums import CollectionNames
from fastapi import Request, HTTPException, status
from models.schemas.product import Product
from typing import Optional


class ProductService(BaseService):
    def __init__(self, request : Request):
        super().__init__()
        self.model = ProductModel(request, CollectionNames.PRODUCTS)

    async def check_product_exist(self, product : Product) -> Optional[dict]:
       
        resulted_product = await self.model.get_product_by_name(product.product_name)
        return resulted_product


    async def add_product(self, product : Product) -> dict:
        
        existing_product = await self.check_product_exist( product = product )

        # Check if product exists on database by the name
        if existing_product:

            # Raise FastAPI HTTPException 
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Product with this name already exists"
            )
 
        new_product = await self.model.add_product( product = product )

        if not new_product:
            raise HTTPException(status_code=500, detail="Product insertion failed.")
        
        # ✅ Transform Mongo document -> Pydantic-compatible
        new_product["product_id"] = str(new_product["_id"])
        new_product.pop("_id", None)

        return new_product
