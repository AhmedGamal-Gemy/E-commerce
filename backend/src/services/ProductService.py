from services.BaseService import BaseService
from models.models.ProductModel import ProductModel
from configs.enums import CollectionNames
from fastapi import Request, HTTPException, status
from models.schemas.product import Product
from typing import Optional, Tuple, Union, List
from bson import ObjectId

class ProductService(BaseService):
    def __init__(self, request : Request):
        super().__init__()
        self.model = ProductModel(request, CollectionNames.PRODUCTS)

    async def check_product_exist(self, product: Union[Product, str]) -> Union[Optional[dict], bool]:
        if isinstance(product, Product):
            return await self.model.get_product_by_name(product.product_name)
        elif isinstance(product, str):
            return await self.model.get_product_by_id(ObjectId(product))
        else:
            raise TypeError("Expected Product or product_id (str)")

    ####################################### NORMAL PAGES #######################################

    async def get_all_products(
            self, 
            current_page: int, 
            products_number_in_page: int,
            last_seen_id : str) -> Tuple[List[Product], int, str]:

        paginated_products = await self.model.get_all_products( 
            current_page = current_page, 
            products_number_in_page = products_number_in_page,
            last_seen_id = last_seen_id
            )
        
        return paginated_products, 
        



    ####################################### ADMIN DASHBOARD #######################################

    async def add_product(self, product : Product) -> dict:
        
        existing_product_by_name = await self.check_product_exist( product = product )

        # Check if product exists on database by the name
        if existing_product_by_name:

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

    async def update_product(self, product_id: str, new_product: Product) -> Tuple[dict, bool]:

        updated_product, did_upsert = await self.model.update_product(product_id = ObjectId(product_id), new_product = new_product )

        if not updated_product:
            raise HTTPException(status_code=500, detail="Product Update failed.")
        
        # ✅ Transform Mongo document -> Pydantic-compatible
        updated_product["product_id"] = str(updated_product["_id"])
        updated_product.pop("_id", None)

        return updated_product, did_upsert
    
    async def delete_product(self, product_id_to_delete: str) -> bool:

        existing_product_by_id = await self.check_product_exist( product = product_id_to_delete )

        # Check if product don't exist on database by the id
        if not existing_product_by_id:

            # Raise FastAPI HTTPException 
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Product with this id don't exist"
            )
        
        is_delete_success = await self.model.delete_product( product_id_to_delete = ObjectId(product_id_to_delete) )

        if not is_delete_success:
            raise HTTPException(status_code=500, detail="Product deletion failed.")

        return is_delete_success
        
