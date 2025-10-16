from configs.enums import CollectionNames
from models.models.BaseModel import BaseModel
from fastapi import Request
from models.schemas.product import Product
from typing import Optional, Tuple, List, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
from math import ceil


class ProductModel(BaseModel):
    def __init__(self, request: Request, collection_name: CollectionNames):
        super().__init__(request, collection_name)

    async def count_all_products(self) -> int:
        products_count = await self.collection.count_documents({})
        return products_count

    async def paginate_products(
        self,
        match_filter: Dict[str, Any],
        products_number_in_page: int,
        last_seen_id: Optional[str] = None
    ) -> Tuple[List[dict], int, Optional[str], int]:
        """
        Generic pagination for products.
        - match_filter: Base query filter (e.g., {} for all, {"product_category_name": category} for filtered).
        - Handles cursor-based pagination, totals, current_page.
        """

        # Compute overall total for consistent total_pages (using base match_filter)
        total = await self.collection.count_documents(match_filter)
        total_pages = ceil(total / products_number_in_page) if total else 0

        if total == 0:
            return [], total_pages, None, 1

        # Create a copy for cursor-modified match
        cursor_match = match_filter.copy()
        if last_seen_id:
            try:
                cursor_oid = ObjectId(last_seen_id)
            except:
                return [], 0, "Invalid_id", 0
            cursor_match["_id"] = {"$gt": cursor_oid}

        # Compute current_page based on items before this cursor (using base match + lte if applicable)
        if last_seen_id:
            prev_filter = match_filter.copy()
            prev_filter["_id"] = {"$lte": cursor_oid}
            previous_count = await self.collection.count_documents(prev_filter)
        else:
            previous_count = 0
        current_page = (previous_count // products_number_in_page) + 1

        # Define consistent projection
        project = {
            "product_id": {"$toString": "$_id"},
            "product_name": 1,
            "product_description": 1,
            "product_price": 1,
            "product_created_at": 1,
            "product_category_name": 1,
            "product_stock_quantity": 1,
            "product_image_path": 1,
            "product_sales": 1
        }

        # Pipeline for data fetch
        pipeline = [
            {"$match": cursor_match},
            {"$sort": {"_id": 1}},
            {"$limit": products_number_in_page},
            {"$project": project}
        ]

        products = []
        cursor = await self.collection.aggregate(pipeline)
        async for document in cursor:
            products.append(document)

        if not products:
            return [], total_pages, None, current_page

        new_last_seen_id = products[-1]["product_id"]

        return products, total_pages, new_last_seen_id, current_page

    async def get_product_by_id(self, product_id: str) -> Optional[dict]:
        """
        Fetch a single product by ID.
        """
        try:
            oid = ObjectId(product_id)
        except:
            return None

        project = {  # Same as above, but without toString since we query by OID
            "product_id": {"$toString": "$_id"},
            "product_name": 1,
            "product_description": 1,
            "product_price": 1,
            "product_created_at": 1,
            "product_category_name": 1,
            "product_stock_quantity": 1,
            "product_image_path": 1,
            "product_sales": 1
        }

        return await self.collection.find_one({"_id": oid}, project)

    async def get_all_products(
        self,
        products_number_in_page: int,
        last_seen_id: Optional[str] = None
    ) -> Tuple[List[dict], int, Optional[str], int]:
        return await self.paginate_products(
            match_filter={},
            products_number_in_page=products_number_in_page,
            last_seen_id=last_seen_id
        )

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

    async def count_products_in_stock(self):
        pipeline = [
            {"$group": {"_id": None, "numOfProductsInTheStock": {"$sum": "$product_stock_quantity"}}}
        ]

        cursor = await self.collection.aggregate(pipeline)
        result = []
        async for document in cursor:
            result.append(document)

        return result[0]["numOfProductsInTheStock"] if result else 0
    
    async def count_sold_products(self):
        pipeline = [
            {"$group": {"_id": None, "total_sales": {"$sum": "$product_sales"}}}
        ]

        cursor = await self.collection.aggregate(pipeline)
        result = []
        async for document in cursor:
            result.append(document)

        return result[0]["total_sales"] if result else 0
    

    async def total_stock_value(self):
        pipeline = [{"$group": {"_id": None, "total": {"$sum": {
            "$multiply": ["$product_stock_quantity", "$product_price"]
        }}}}]

        cursor = await self.collection.aggregate(pipeline)
        result = []
        async for document in cursor:
            result.append(document)

        return result[0]["total"] if result else 0

    async def total_sold_value(self):
        pipeline = [{"$group": {"_id": None, "total": {"$sum": {
            "$multiply": ["$product_sales", "$product_price"]
        }}}}]
        
        cursor = await self.collection.aggregate(pipeline)
        result = []
        async for document in cursor:
            result.append(document)


        return result[0]["total"] if result else 0


    async def most_sold_product(self):
        doc = await self.collection.find_one(
            sort=[("product_sales", -1)],
        )
        if not doc:
            return None

        # ✅ Convert ObjectId to string for JSON serialization
        doc["product_id"] = str(doc["_id"])
        del doc["_id"]
        return doc

