from fastapi import Request
from fastapi.responses import JSONResponse

# If we have a lot of Exception types, we can collect this in domain __init__.py
from app.domain.contracts import InvalidLicenseDate


class ExceptionHandlers:
    exception_handlers = set()

    def register(self, handler):
        self.exception_handlers.add(handler)


@ExceptionHandlers.register
async def license_exception_handler(_: Request, exc: InvalidLicenseDate):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
