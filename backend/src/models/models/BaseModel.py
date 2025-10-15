from fastapi import Request
from core.Base import Base
from configs.enums import CollectionNames


class BaseModel(Base):

    def __init__(self, request : Request, collection_name: CollectionNames):

        super().__init__()
        
        if not hasattr(request.app, "db_client"):
            raise RuntimeError("Database client not initialized in app.")
        

        self.db_client = request.app.db_client
        self.collection = self.db_client[collection_name.value]
