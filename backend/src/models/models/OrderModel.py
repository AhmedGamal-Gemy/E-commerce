from models.models.BaseModel import BaseModel
from models.schemas.order import Order
from configs.enums import CollectionNames
from fastapi import Request
from typing import List, Optional
from api.schemas.RequestSchemas import OrderItemRequest
from bson import ObjectId
from models.models.ProductModel import ProductModel


class OrderModel(BaseModel):

    def __init__(self, request : Request):

        super().__init__( request = request, collection_name= CollectionNames.ORDERS )
        self.logger.info(f"OrderModel initialized")
        self.product_model = ProductModel(request, collection_name=CollectionNames.PRODUCTS)
        self.product_collection = product_model.collection
        

    async def calculate_total(self, order_items: List[OrderItemRequest]) -> float:
        """
        Calculate the total price for all order items.
        Each product price is fetched from MongoDB and multiplied by its quantity.
        """
        total = 0.0

        # Prepare a set of product IDs for one bulk query
        product_ids = [ObjectId(item.product_id) for item in order_items]

        # Fetch all matching products in one query
        products_cursor = self.product_collection.find({"_id": {"$in": product_ids}})

        result = []
        async for document in products_cursor:
            result.append(document)


        # Map product_id → price for quick lookup
        product_price_map = {
            str(product["_id"]): product["product_price"]
            for product in result
        }

        product_stock_quantity_map = {
            str(product["_id"]): product["product_stock_quantity"]
            for product in result
        }

        # Calculate total amount
        for item in order_items:
            product_id = item.product_id
            quantity = item.quantity
            product_stock_quantity = product_stock_quantity_map.get(product_id)
            price = product_price_map.get(product_id)

            if price is None or product_stock_quantity is None:
                raise ValueError(f"Product with id {product_id} not found.")

            if product_stock_quantity < quantity:
                raise ValueError(f"Insufficient stock for product {product_id}")

            total += price * quantity

        return round(total, 2)

    async def create_order(self, order : Order) -> Optional[Order]:

        order_data = order.model_dump( mode = "json" )
        
        result = await self.collection.insert_one(order_data)

        if result.inserted_id:
            created_order = await self.collection.find_one({"_id": result.inserted_id})

        else:
            self.logger.error("Failed to insert order.")
            return None
    
        # ✅ Transform Mongo document -> Pydantic-compatible
        created_order["order_id"] = str(created_order["_id"])
        created_order.pop("_id", None)

        return Order(**created_order)
    
    async def update_product_stock_sales(self, product_id: str, sold_quantity: int) -> bool:
        
        old_product = await self.product_model.get_product_by_id(product_id = product_id)
        
        result = self.product_collection.update_one(
                filter = {"_id" : product_id },
                update = {
                    "product_stock_quantity" : ( int(old_product["product_stock_quantity"] ) - sold_quantity),
                    "product_sales" : ( int(old_product["product_sales"]) + sold_quantity )
                }
            )
        
        if result.matched_count > 0:
            return True
        else:
            return False
