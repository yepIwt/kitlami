from blacksheep import auth
from blacksheep.server.controllers import get, patch, post
from guardpost.authentication import Identity

from kitlami.app.auth.models import User
from kitlami.app.core.controllers import ApiController
from kitlami.auth.handlers import decode_token, generate_tokens
from kitlami.auth.hash import get_password_hash
from kitlami.db.connection import Transaction
from kitlami.exceptions import (
    PasswordMatchError,
    UserAlreadyRegistered,
    UserNotFoundError,
)
from kitlami.protocol import Response

from .views import (
    TokenRequestView,
    TokenResponseView,
    UpdateProfileView,
    UserLoginView,
    UserProfileView,
)


class AuthorizationController(ApiController):
    @post("/auth/refresh-token")
    async def refresh_token(
        self, body: TokenRequestView
    ) -> Response[TokenResponseView]:
        token = decode_token(body.refresh_token)
        async with Transaction():
            user = await User.get_by_id(token.sub)

        if not user:
            raise UserNotFoundError

        return Response(
            payload=generate_tokens(
                sub=str(user.id),
                email=user.email,
                first_name=user.first_name,
                last_name=user.first_name,
            )
        )

    @post("/auth/registration")
    async def registration(self, body: UserLoginView) -> Response:
        async with Transaction():
            user = await User.get_by_email(body.email)
            if user:
                raise UserAlreadyRegistered

            user_id = await User.create(
                email=body.email,
                hashed_password=get_password_hash(body.password),
            )
        return Response(payload=generate_tokens(sub=str(user_id), email=body.email))

    @post("/auth/login")
    async def login(self, body: UserLoginView) -> Response:
        async with Transaction():
            user = await User.get_by_email(body.email)

        if not user:
            raise UserNotFoundError

        hashed_password = get_password_hash(body.password)

        if user.hashed_password == hashed_password:
            return Response(
                payload=generate_tokens(
                    sub=str(user.id),
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.first_name,
                )
            )

        raise PasswordMatchError

    @auth(User.UserRole.USER)
    @get("/profile")
    async def get_profile(self, user: Identity) -> Response[UserProfileView]:
        async with Transaction():
            user = await User.get_by_email(user.claims["email"])
            return Response(payload=UserProfileView.from_orm(user))

    @auth(User.UserRole.USER)
    @patch("/profile")
    async def edit_profile(
        self, token_user: Identity, body: UpdateProfileView
    ) -> Response[UserProfileView]:
        async with Transaction():
            user = await User.get_by_id(token_user.claims["sub"])

            await user.update(
                user_id=user.id,
                first_name=body.first_name or user.first_name,
                last_name=body.last_name or user.last_name,
                picture_url=body.picture_url or user.picture_url,
            )
            return Response(payload=UserProfileView.from_orm(user))
