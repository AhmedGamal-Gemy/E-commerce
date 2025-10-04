from fastapi import FastAPI

from contextlib import asynccontextmanager

from configs.settings import get_settings
from core.logging import get_logger
from utils.init_database import init_database

from api.routes.login_router import login_router

def create_app() -> FastAPI:

    settings = get_settings()

    logger = get_logger(__name__)

    logger.info(f"Starting application: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")

    @asynccontextmanager    
    async def lifespan(app: FastAPI):
        # Startup code
        logger.info("Application startup")
        app.db_conn, app.db_client = await init_database()

        yield
        # Shutdown code
        logger.info("Application shutdown") 
        await app.db_conn.close()

    app = FastAPI( lifespan=lifespan )

    app.include_router( login_router )