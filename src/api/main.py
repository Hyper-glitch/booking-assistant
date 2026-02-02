import asyncio
import logging

import uvicorn
import uvloop

from api.app import app
from api.logger import setup_logger
from api.settings import settings

logger = logging.getLogger(__name__)


async def main() -> None:
    """The main entry point for configuring and launching the app."""
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            host=settings.APP_HOST,
            port=settings.APP_PORT,
            reload=settings.DEBUG,
        )
    )
    logger.info(f"server_started host={settings.APP_HOST}, port={settings.APP_PORT}")
    try:
        await server.serve()
    except Exception as exc:
        logger.error(f"server_error, error={exc}")


if __name__ == "__main__":
    uvloop.install()
    setup_logger()
    asyncio.run(main(), debug=settings.DEBUG)
