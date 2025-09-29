from pydantic import BaseModel, Field
from bson import ObjectId

class Category(BaseModel):
    category_id : ObjectId
    category_name : str
    category_description : str

