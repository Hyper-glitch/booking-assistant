import asyncio

import uvicorn
import uvloop
from logger import logger

from api.app import app
from api.logger import setup_logger
from api.settings import settings


async def main() -> None:
    """The main entry point for configuring and launching the app."""
    setup_logger()
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            reload=settings.DEBUG,
        )
    )
    logger.info("server_started", host=settings.APP_HOST, port=settings.APP_PORT)
    try:
        await server.serve()
    except Exception as exc:
        logger.error("server_error", error=str(exc), exc_info=True)


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(main(), debug=settings.DEBUG)
