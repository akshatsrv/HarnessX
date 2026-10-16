from fastapi import Request
from fastapi.responses import JSONResponse


class ClaimGuardException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


async def claimguard_exception_handler(request: Request, exc: ClaimGuardException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.message, "path": str(request.url.path)}
    )
