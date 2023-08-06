from functools import (
    wraps,
)
from loguru import (
    logger,
)
from typing import (
    Dict,
)
from yaml import (
    safe_load,
    YAMLError,
)


def load_yaml(file: str) -> Dict:
    with open(file, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as error:
            print(error)
            logger.error("Error while loading yaml file")
            exit(1)


def load_config() -> Dict:
    return load_yaml("./setup.yml")


def log_step(step):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            logger.info(f"Setting up {step}")
            function(*args, **kwargs)
            logger.success(f"Successfully configured {step}")
            return

        return wrapper

    return inner_function
