from typing import Optional
from pydantic import BaseModel, Field
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    authjwt_secret_key: str = "secretkey"


@AuthJWT.load_config
def get_config():
    return Settings()


class RegisterSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[str] = None
    role: Optional[str] = None
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class LoginSchem(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
