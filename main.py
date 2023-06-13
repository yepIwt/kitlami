from blacksheep import Application, Request, json
from blacksheep.server.authorization import Policy
from guardpost import UnauthorizedError
from guardpost.common import AuthenticatedRequirement

from kitlami import exceptions
from kitlami.app.auth.controllers import AuthorizationController
from kitlami.auth.handlers import AuthHandler
from kitlami.docs import docs
from kitlami.logger import logger
from kitlami.protocol import Response as MyResponse

app = Application()

app.register_controllers([AuthorizationController])

docs.bind_app(app)

app.use_cors(
    allow_methods="*",
    allow_origins="*",
    allow_headers="* Authorization",
    max_age=300,
)

app.use_authentication().add(AuthHandler())
app.use_authorization().add(Policy("user", AuthenticatedRequirement()))


@app.exception_handler(Exception)
async def uvicorn_base_exception_handler(self, request: Request, exc: Exception):
    logger.debug(exc)
    error = exceptions.ServerError(message=str(exc))
    return json(
        MyResponse(
            code=error.status_code,
            message=error.message,
            exception_class="ServerError",
        ).dict()
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(
    self, request: Request, exc: exceptions.ApiException
):
    logger.debug(exc.message)

    return json(
        MyResponse(
            code=exc.status_code, message=exc.message, exception_class=exc._type()
        ).dict()
    )


@app.exception_handler(UnauthorizedError)
async def guardpost_api_exception_handler(
    self, request: Request, exc: UnauthorizedError
):
    logger.debug(exc)
    error = exceptions.UnauthorizedError()
    return json(
        MyResponse(
            code=error.status_code,
            message=error.message,
            exception_class=error._type(),
        ).dict()
    )


@app.exception_handler(400)
async def validation_exception_handler(self, request: Request, exc):
    logger.debug(exc)
    error = exceptions.ValidationError(message=str(exc))
    return json(
        MyResponse(
            code=error.status_code,
            message=error.message,
            exception_class=error._type(),
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000)
