import time
from datetime import datetime

import jwt
from blacksheep import Request
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from pydantic import ValidationError

from kitlami.app.auth.views import (
    AccessTokenView,
    RefreshTokenView,
    TokenResponseView,
    TokenType,
)
from kitlami.auth.hash import encode_jwt
from kitlami.config import settings
from kitlami.exceptions import JWTDecodeError, JWTExpiredSignatureError, UnauthorizedError


class AuthHandler(AuthenticationHandler):
    def __init__(self):
        pass

    async def authenticate(self, context: Request) -> Identity | None:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            token = header_value.decode().split()[-1]
            decoded_data = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG], options={"verify_signature": True}
            )
            context.identity = Identity(claims=decoded_data, authentication_mode="access_token")
        else:
            context.identity = None
        return context.identity


def get_exp_time(token_type: TokenType) -> int:
    now = datetime.now()

    if token_type == TokenType.ACCESS:
        now += settings.ACCESS_TOKEN_EXP
    if token_type == TokenType.REFRESH:
        now += settings.REFRESH_TOKEN_EXP

    return int(now.timestamp())


def generate_tokens(sub: str, email: str, first_name: str | None = None, last_name: str | None = None) -> dict:
    access_token_view = AccessTokenView(
        sub=sub,
        exp=get_exp_time(token_type=TokenType.ACCESS),
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    refresh_token_view = RefreshTokenView(
        sub=sub,
        exp=get_exp_time(token_type=TokenType.REFRESH),
    )

    access_token = encode_jwt(access_token_view)
    refresh_token = encode_jwt(refresh_token_view)

    return TokenResponseView(
        access_token=access_token,
        refresh_token=refresh_token,
        exp=access_token_view.exp,
    )


def decode_token(token: str) -> RefreshTokenView:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG], options={"verify_signature": True}
        )
        if not payload:
            raise UnauthorizedError
        token_data = RefreshTokenView(**payload)
        if time.time() > token_data.exp:
            raise JWTExpiredSignatureError

    except jwt.ExpiredSignatureError as e:
        raise JWTExpiredSignatureError from e
    except jwt.DecodeError as e:
        raise JWTDecodeError from e
    except ValidationError as e:
        raise UnauthorizedError from e

    return token_data
