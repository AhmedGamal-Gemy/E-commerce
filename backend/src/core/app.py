from fastapi import FastAPI

from contextlib import asynccontextmanager

from configs.settings import get_settings
from core.logging import get_logger
from utils.init_database import init_database

from api.routes.auth_router import AuthRouter

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


    app = FastAPI( lifespan = lifespan )

    auth = AuthRouter()

    app.include_router( auth.get_auth_router() )


    return app