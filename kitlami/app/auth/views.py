import uuid
from enum import StrEnum

from pydantic import EmailStr

from kitlami.config import settings
from kitlami.protocol import BaseModel


class TokenRequestView(BaseModel):
    access_token: str
    refresh_token: str


class TokenResponseView(BaseModel):
    access_token: str
    refresh_token: str
    exp: int


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class UserLoginView(BaseModel):
    email: EmailStr
    password: str


class AccessTokenView(BaseModel):
    iss: str = settings.APP_NAME
    sub: str | uuid.UUID
    exp: int
    email: EmailStr
    first_name: str | None
    last_name: str | None


class RefreshTokenView(BaseModel):
    iss: str = settings.APP_NAME
    sub: str | uuid.UUID
    exp: int


class UpdateProfileView(BaseModel):
    first_name: str | None
    last_name: str | None
    picture_url: str | None


class UserProfileView(BaseModel):
    first_name: str | None
    last_name: str | None
    picture_url: str | None
    email: str
