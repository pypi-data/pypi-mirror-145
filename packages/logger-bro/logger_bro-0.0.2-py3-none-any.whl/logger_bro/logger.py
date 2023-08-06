import logging
from typing import Union
import logging_loki
from multiprocessing import Queue
from logger_bro.settings import get_settings

settings = get_settings()

handler = logging_loki.LokiQueueHandler(
    Queue(-1),
    url=settings.LOKI,
    # TODO: Create versioning for the logger. We need different logs
    # for v1 and v2
    tags={"application": "WSMA", "version": "v1"},
    # Version is used internally by the client. It is irrelevant
    # to the api version
    version="1",
)


logger = logging.getLogger("loki")
logger.setLevel(level=logging.INFO)
logger.addHandler(handler)


def get_loki_logger():
    return logging.getLogger("loki")


def log_exception(exc: Exception):
    logger = get_loki_logger()
    logger.exception(
        exc, extra={"tags": {"level": logging.getLevelName(logging.ERROR)},},
    )
