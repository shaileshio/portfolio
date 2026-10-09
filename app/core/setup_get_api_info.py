from collections.abc import Mapping
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


class FrozenBaseModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class EndpointMethodInfo(FrozenBaseModel):
    summary: str | None = None
    description: str | None = None


class EndpointInfo(FrozenBaseModel):
    path: str
    methods: dict[str, EndpointMethodInfo]


class APIInfoResponse(FrozenBaseModel):
    version: str
    name: str
    description: str | None = None
    endpoints: list[EndpointInfo]


HTTP_METHODS = frozenset(
    {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD", "TRACE"}
)


def discover_endpoints(
    openapi_schema: Mapping[str, Any],
    *,
    exclude_paths: frozenset[str] = frozenset({"/"}),
) -> list[EndpointInfo]:
    endpoints: list[EndpointInfo] = []

    for path, path_item in openapi_schema.get("paths", {}).items():
        if path in exclude_paths:
            continue

        methods: dict[str, EndpointMethodInfo] = {}

        for method, operation in path_item.items():
            normalized_method = method.upper()

            if normalized_method not in HTTP_METHODS:
                continue

            methods[normalized_method] = EndpointMethodInfo(
                summary=operation.get("summary"),
                description=operation.get("description"),
            )

        if not methods:
            continue

        endpoints.append(
            EndpointInfo(
                path=path,
                methods=dict(sorted(methods.items())),
            )
        )

    return endpoints


def setup_get_api_info(app: FastAPI) -> None:
    @app.get(
        "/",
        tags=["API Discovery"],
        summary="Discover available API endpoints",
        description="Returns basic metadata for documented API endpoints.",
        include_in_schema=False,
    )
    async def get_api_info() -> APIInfoResponse:
        endpoints = discover_endpoints(app.openapi())

        return APIInfoResponse(
            name=app.title,
            version=app.version,
            description=app.description,
            endpoints=endpoints,
        )
