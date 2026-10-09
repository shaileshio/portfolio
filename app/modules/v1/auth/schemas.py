from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.db.base import BaseOrmModel


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


class UserResponse(BaseOrmModel):
    id: UUID
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogout(BaseModel):
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
