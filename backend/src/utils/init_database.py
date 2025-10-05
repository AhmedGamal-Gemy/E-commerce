from fastapi import Request

from pymongo import AsyncMongoClient

from configs.settings import get_settings
from urllib.parse import quote_plus

async def init_database():

    settings = get_settings()

    username = quote_plus(settings.DB_USER)
    password = quote_plus(settings.DB_PASSWORD)
    host = settings.DB_HOST
    db_name = settings.DB_NAME

    mongo_uri = (
        f"mongodb://{username}:{password}@{host}:27017/{db_name}?authSource=admin"
    )

    # init_indexes()
    
    mongo_conn = AsyncMongoClient(mongo_uri)
    db_client = mongo_conn[db_name]

    return mongo_conn, db_client

# async def init_indexes(db_client : object):

#     model_collection_map = {
#         User : 
#         Product : DatabaseEnum.COLLECTION_PROJECT_NAME.value,
#         Category : DatabaseEnum.COLLECTION_ASSET_NAME.value
#     }

#     for model, collection_name in model_collection_map.items():

#         indexes = model.get_indexes()
#         if indexes:
#             collection = db_client[ collection_name ]
#             await collection.create_indexes( indexes )


async def get_db(request : Request):
    return request.app.db