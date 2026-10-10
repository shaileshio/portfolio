from pydantic import BaseModel


class DetailResponse(BaseModel):
    detail: str


class Meta(BaseModel):
    pass


class Response[D](BaseModel):
    data: D
    meta: Meta
