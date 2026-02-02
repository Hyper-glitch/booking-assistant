import logging

from api.settings import settings

logger = logging.getLogger("api")


def setup_logger() -> None:
    """Set up the logger to stdout output."""
    formatter = logging.Formatter(
        "[%(process)d] [%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(handler)
