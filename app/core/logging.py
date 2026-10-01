from logging.config import dictConfig
from sys import stdout
from typing import Any, Literal

from app.core.config import get_settings

settings = get_settings()
debug = settings.app.env != "production"


LOG_LEVEL: Literal["DEBUG", "INFO"] = "DEBUG" if debug else "INFO"

LOGGING_CONFIG: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": ("%(asctime)s %(levelname)s %(name)s %(message)s"),
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "stream": stdout,
            "formatter": "default",
        },
    },
    "loggers": {
        # Your application logs
        "app": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # FastAPI / Uvicorn application errors
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # HTTP access logs
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
    # Catch libraries that don't have their own logger configuration.
    "root": {
        "handlers": ["default"],
        "level": LOG_LEVEL,
    },
}


def configure_logging() -> None:
    dictConfig(config=LOGGING_CONFIG)
