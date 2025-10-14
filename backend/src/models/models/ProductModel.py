from configs.enums import CollectionNames
from models.models.BaseModel import BaseModel
from fastapi import Request
from models.schemas.product import Product
from typing import Optional, Tuple
from datetime import datetime, timezone

class ProductModel(BaseModel):
    def __init__(self, request: Request, collection_name: CollectionNames):
        super().__init__(request, collection_name)

    async def count_all_products(self) -> int:
        products_count = await self.collection.count_documents({})
        return products_count


    async def get_all_products(self, current_page: int, products_number_in_page :int, last_seen_id: str ):
        
        # Check if there's no products
        if await self.count_all_products() <= 0:
            return

        pass

    async def get_product_by_name(self, product_name : str):

        resulted_product = await self.collection.find_one({"product_name" : product_name})

        if resulted_product:
            return resulted_product
        return None
    
    async def get_product_by_id(self, product_id : str):

        resulted_product = await self.collection.find_one({"_id" : product_id})

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

    async def update_product(self, product_id: str, new_product: Product) -> Tuple[Optional[Product], bool]:
        product_data = new_product.model_dump( mode = "json" )

        query_filter = {
            "_id" : product_id
        }

        update_operation = { '$set' : product_data }

        result = await self.collection.update_one(query_filter, update_operation, upsert = True)
        
        updated_product = await self.collection.find_one({"_id": product_id})

        return updated_product, result.did_upsert
    
    async def delete_product(self, product_id_to_delete: str)-> bool:

        query_filter = {
            "_id" : product_id_to_delete
        }

        result = await self.collection.delete_one(query_filter)

        return result.deleted_count > 0


