from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


class RegisterResponse(BaseModel):
    id: UUID
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class LogoutRequest(BaseModel):
    refresh: str
    access: str
