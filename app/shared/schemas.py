from pydantic import BaseModel, Field


class DetailResponse(BaseModel):
    detail: str


class PaginationMeta(BaseModel):
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    total: int = Field(ge=0)
    has_more: bool
    next_offset: int | None = None


class Meta(BaseModel):
    pagination: PaginationMeta
