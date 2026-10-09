from fastapi import FastAPI

from app.core.config import get_settings
from app.core.exceptions.handlers import setup_error_handlers
from app.core.logging import configure_logging
from app.core.middlewares import setup_middlewares
from app.modules.router import router

configure_logging()

settings = get_settings()

title = settings.app.title
description = settings.app.description
debug = settings.app.env != "production"


def create_app() -> FastAPI:
    app = FastAPI(
        title=title,
        description=description,
        debug=debug,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    setup_error_handlers(app)
    setup_middlewares(app)

    app.include_router(router)

    return app


app = create_app()
