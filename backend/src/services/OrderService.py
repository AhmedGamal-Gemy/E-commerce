from services.BaseService import BaseService
from models.models.OrderModel import OrderModel
from models.schemas.order import Order
from fastapi.requests import Request



class OrderService(BaseService):
    
    def __init__(self, request : Request):
        super().__init__()
        self.model = OrderModel(request)


                