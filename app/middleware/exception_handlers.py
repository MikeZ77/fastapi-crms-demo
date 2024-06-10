from typing import Callable, TypeAlias

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

# If we have a lot of Exception types, we can collect this in domain __init__.py
from app.domain.contracts import InvalidLicenseDate

ExcHandlerType: TypeAlias = Callable[[Request, Exception], Response]


class ExceptionHandlers:
    exception_handlers: set[Exception, ExcHandlerType] = set()

    @classmethod
    def register(cls, exc_type: Exception):
        def inner(handler: ExcHandlerType):
            cls.exception_handlers.add((exc_type, handler))

        return inner

    @classmethod
    def register_exception_handlers(cls, app: FastAPI):
        for exc_type, handler in cls.exception_handlers:
            app.add_exception_handler(exc_type, handler)


@ExceptionHandlers.register(InvalidLicenseDate)
async def license_exception_handler(_: Request, exc: InvalidLicenseDate):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
