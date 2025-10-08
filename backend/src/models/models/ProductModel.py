from configs.enums import CollectionNames
from models.models.BaseModel import BaseModel
from fastapi import Request
from models.schemas.product import Product
from typing import Optional
from datetime import datetime, timezone

class ProductModel(BaseModel):
    def __init__(self, request: Request, collection_name: CollectionNames):
        super().__init__(request, collection_name)

    async def get_product_by_name(self, product_name : str):

        resulted_product = await self.collection.find_one({"product_name" : product_name})

        if resulted_product:
            return resulted_product
        return None

    async def add_product(self, product : Product) -> Optional[Product]:

        product_data = product.model_dump( mode = "json" )
        product_data["product_created_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(product_data)

        if result.inserted_id:
            created_product = await self.collection.find_one({"_id": result.inserted_id})
            return created_product
        else:
            self.logger.error("Failed to insert product.")
            return None

