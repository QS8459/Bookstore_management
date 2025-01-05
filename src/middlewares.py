from fastapi import Request, Response, HTTPException, Depends
from starlette.responses import JSONResponse
from time import perf_counter
from src.logfunc import logger
from src.service.users.users import users_service
from starlette.middleware.base import BaseHTTPMiddleware


class Cookie_checker(BaseHTTPMiddleware):
    def __init__(self, app, exclude_routes = None):
        super().__init__(app)
        self.exclude_routes = exclude_routes or []

    async def dispatch(self, request: Request, call_next, usr_service = Depends(users_service)):
        cookie_value = request.headers.get("Cookie")
        if request.url.path in self.exclude_routes:
            return await call_next(request)
        if cookie_value:
            usr_service.decode_cookie(cookie_value)
            response = await call_next(request)
            return response
        return JSONResponse(
            status_code = 401,
            content = {
                'base_url': f'{request.headers.get("host")}/api/v1/user/visit'
            }
        )
async def ip_cookie(request: Request, call_next):
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    response.headers.update({"X-Process-Time":f"{process_time}"})
    logger.info(f"Process time {process_time}")
    return response

async def log_exception(request: Request, call_next):
    try:
        logger.info(f"{request.method}: at {request.url.path}")
        response = await call_next(request)
    except HTTPException as e:
        # Log the exception here
        logger.error(f"Exception occurred: at {request.url.path}: {str(e)}")
        # Return a custom error response
        return JSONResponse(
            content={"detail": "An internal error occurred."},
            status_code=500,
        )
    return response
