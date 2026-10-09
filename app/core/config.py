from functools import lru_cache
from typing import Literal

from cryptography.fernet import Fernet
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    title: str = "Portfolio"
    description: str = "Software Engineering Portfolio"
    env: Literal["test", "development", "production"] = "production"


class CorsConfig(BaseModel):
    allow_origins: list[str] = ["127.0.0.1", "localhost"]
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]
    allow_credentials: bool = True


class DatabaseConfig(BaseModel):
    url: str | None = None
    test_url: str | None = None

    def get_url(self) -> str:
        if self.url is None:
            raise RuntimeError("Database URL is not configured.")

        return self.url

    def get_test_url(self) -> str:
        if self.test_url is None:
            raise RuntimeError("Test database URL is not configured.")

        return self.test_url


class AuthConfig(BaseModel):
    jwt_secret_key: str = Fernet.generate_key().decode()
    jwt_hashing_algorithm: str = "HS256"

    access_token_lifetime: float = 30
    refresh_token_lifetime: float = 60 * 7
    session_lifetime: float = 60 * 720


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppConfig = Field(default_factory=AppConfig)
    cors: CorsConfig = Field(default_factory=CorsConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)


@lru_cache
def get_settings() -> Settings:
    return Settings()
