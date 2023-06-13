from hashlib import sha256

import jwt

from kitlami.app.auth.views import AccessTokenView, RefreshTokenView
from kitlami.config import settings


def get_password_hash(password: str):
    return sha256(password.encode()).hexdigest()


def encode_jwt(payload: AccessTokenView | RefreshTokenView):
    return jwt.encode(payload.dict(), settings.JWT_SECRET, algorithm=settings.JWT_ALG)
