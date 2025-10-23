from services.BaseService import BaseService
from models.models.ProductModel import ProductModel
from configs.enums import CollectionNames
from fastapi import Request, HTTPException, status
from models.schemas.product import Product
from typing import Optional, Tuple, Union, List, Dict
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
            products_number_in_page: int,
            last_seen_id : str) -> Tuple[List[dict], int, Optional[str], int]:

        paginated_products, total_pages, new_last_seen_id, current_page = await self.model.get_all_products( 
            products_number_in_page = products_number_in_page,
            last_seen_id = last_seen_id
            )

        return paginated_products, total_pages, new_last_seen_id, current_page
        
    async def get_product_by_id(
        self,
        product_id: str
    )-> Optional[Dict]:
        
        product = await self.model.get_product_by_id(product_id=product_id)

        if not product:
            return HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "There's no product with this id"

            )
        return product

    async def get_products_by_category(
        self,
        category: str,
        products_number_in_page: int,
        last_seen_id: Optional[str] = None
    ) -> Tuple[List[dict], int, Optional[str], int]:
        return await self.model.paginate_products(
            match_filter={"product_category_name": category},
            products_number_in_page=products_number_in_page,
            last_seen_id=last_seen_id
        )

    async def search_products_by_query(
            self,
            query: str, 
            products_number_in_page: int,
            last_seen_id: Optional[str] = None
            ):
        match_stage = {
            "product_name": {"$regex": query, "$options": "i"},
            "_id": {"$gt": ObjectId(last_seen_id)} if last_seen_id else {"$exists": True}
        }
        return await self.model.paginate_products(
            match_filter= match_stage,
            products_number_in_page=products_number_in_page
            )
        

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
        
    async def get_basic_analysis(self):
        num_in_stock = await self.model.count_products_in_stock()
        num_sold = await self.model.count_sold_products()
        total_stock_value = await self.model.total_stock_value()
        total_sold_value = await self.model.total_sold_value()
        most_sold = await self.model.most_sold_product()

        most_sold_product = Product(
            **most_sold
        ) if most_sold else None

        return {
            "numOfProductsInTheStock": num_in_stock,
            "numOfSaledProducts": num_sold,
            "totalPriceOfAllProductsInTheStock": total_stock_value,
            "totalPriceOfSaledProducts": total_sold_value,
            "theMostSaledProduct": most_sold_product,
        }