from functools import (
    wraps,
)
from loguru import (
    logger,
)


def log_info(message: str) -> str:
    logger.info(message)
    return message


def log_error(message: str) -> None:
    logger.error(message)


def log_success(message: str) -> None:
    logger.success(message)


def log_step(step: str):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            log_info(f"Setting up {step}")
            function(*args, **kwargs)
            log_success(f"Successfully configured {step}")

        return wrapper

    return inner_function
