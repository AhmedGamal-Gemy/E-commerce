from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from configs.settings import get_settings
from core.logging import get_logger
from utils.init_database import init_database

from api.routes.auth_router import AuthRouter
from api.routes.product_router import ProductRouter


def create_app() -> FastAPI:

    settings = get_settings()

    logger = get_logger(__name__)

    logger.info(f"Starting application: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")

    @asynccontextmanager
    async def lifespan(app : FastAPI):

        # Before the app receiveing requests
        app.mongo_conn, app.db_client = await init_database()
        print("Connected DBs:", await app.db_client.list_collection_names())

        yield

        # After the app ends
        await app.mongo_conn.close()


    app = FastAPI( 
        title = settings.PROJECT_NAME,
        version = settings.PROJECT_VERSION,
        lifespan = lifespan
        )

    auth = AuthRouter()
    product = ProductRouter()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For development - allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allows all headers
    )


    app.include_router( auth.get_auth_router() )
    app.include_router( product.get_product_router() )



    return app