from pydantic import BaseModel


class AuthCredentials(BaseModel):
    email: str
    password: str
