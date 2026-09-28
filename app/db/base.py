from typing import Any

from pydantic import BaseModel as Model
from pydantic import ConfigDict
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=NAMING_CONVENTION,
    )

    def __init_subclass__(cls, *, name: str, **kwargs: dict[str, Any]) -> None:
        if not name:
            raise ValueError(f"{cls.__name__}: table name cannot be empty")

        cls.__tablename__ = name

        super().__init_subclass__(**kwargs)


class BaseModel(Model):
    model_config = ConfigDict(
        from_attributes=True,
    )
