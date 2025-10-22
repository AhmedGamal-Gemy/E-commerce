from models.models.BaseModel import BaseModel
from models.schemas.order import Order
from configs.enums import CollectionNames
from fastapi import Request


class OrderModel(BaseModel):

    def __init__(self, request : Request):

        super().__init__( request = request, collection_name= CollectionNames.ORDERS )

        self.logger.info(f"OrderModel initialized")
        


