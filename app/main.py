from fastapi import FastAPI

from app.core.config import Settings, get_settings
from app.core.exceptions.handlers import setup_error_handlers
from app.core.logging import configure_logging
from app.core.middlewares import setup_middlewares
from app.core.swagger import setup_swagger_ui
from app.modules.router import router

configure_logging()

settings: Settings = get_settings()

title: str = settings.app.title
description: str = settings.app.description
debug: bool = settings.app.debug


def create_app() -> FastAPI:
    app = FastAPI(
        title=title,
        description=description,
        debug=debug,
        docs_url=None,
    )

    setup_error_handlers(app)
    setup_middlewares(app)
    setup_swagger_ui(app)

    app.include_router(router)

    return app


app: FastAPI = create_app()
