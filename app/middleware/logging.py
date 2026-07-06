import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log request method, path, status code,
    and processing time.
    """

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            "%s %s %s %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response