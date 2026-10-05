from fastapi import HTTPException, Request, FastAPI
from fastapi.responses import JSONResponse

from core.exceptions import *


def set_exc_handlers(router: FastAPI):

    @router.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        raise HTTPException(
                status_code=429,
                detail=str(exc.message),
                headers={"Retry-After": str(max(exc.retry_after, 1))}
            )

    @router.exception_handler(RateLimiterUnavailable)
    async def limiter_down_handler(request: Request, exc: RateLimiterUnavailable):
        return JSONResponse(status_code=503, content={"detail": "Service unavailable"})


    @router.exception_handler(UserAlreadyExistsException)
    async def limiter_down_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": str(exc.message)})

    
    @router.exception_handler(ServiceException)
    async def limiter_down_handler(request: Request, exc: ServiceException):
        return JSONResponse(status_code=500, content={"detail": str(exc.message)})


    @router.exception_handler(InvalidDataForLoginException)
    async def limiter_down_handler(request: Request, exc: InvalidDataForLoginException):
        return JSONResponse(status_code=401, content={"detail": str(exc.message)})


    @router.exception_handler(ServerBadGetwayException)
    async def limiter_down_handler(request: Request, exc: ServerBadGetwayException):
        return JSONResponse(status_code=502, content={"detail": str(exc.message)})


    @router.exception_handler(NotFoundException)
    async def limiter_down_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc.message)})


    @router.exception_handler(UnauthorizedException)
    async def limiter_down_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=401, content={"detail": str(exc.message)})




