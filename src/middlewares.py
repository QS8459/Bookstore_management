from fastapi import Request, Response, HTTPException
from starlette.responses import JSONResponse
from time import perf_counter
from src.logfunc import logger
from src.db.models.users.cookie import Cookie

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
