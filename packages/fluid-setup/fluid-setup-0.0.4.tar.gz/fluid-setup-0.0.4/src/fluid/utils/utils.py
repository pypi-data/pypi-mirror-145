from functools import (
    wraps,
)
from loguru import (
    logger,
)
from os.path import (
    exists,
)
from typing import (
    Dict,
)
from wget import (
    download,
)
from yaml import (
    safe_load,
    YAMLError,
)


def download_config():
    logger.info("Fetching default setup configuration")
    url = "https://raw.githubusercontent.com/afgalvan/fluid-setup/main/setup.yml?token=GHSAT0AAAAAABQ7JAZBW5MZUO4LXMM6B4GIYSRYOEA"
    download(url)


def load_yaml(file: str) -> Dict:
    with open(file, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as error:
            print(error)
            logger.error("Error while loading yaml file")
            exit(1)


def load_config() -> Dict:
    if not exists("./setup.yml"):
        download_config()
    return load_yaml("./setup.yml")


def log_step(step):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            logger.info(f"Setting up {step}")
            function(*args, **kwargs)
            logger.success(f"Successfully configured {step}")

        return wrapper

    return inner_function
