from __future__ import annotations

from datetime import date

import loguru
from loguru import logger


def get_logger() -> loguru.Logger:
    """
    Creates logger object.

    @return: logger
    """
    today = date.today().strftime("%d-%d-%Y")
    logger.add(
        f"logs/{str(today)}.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        colorize=True,
        level="DEBUG",
    )
    return logger
