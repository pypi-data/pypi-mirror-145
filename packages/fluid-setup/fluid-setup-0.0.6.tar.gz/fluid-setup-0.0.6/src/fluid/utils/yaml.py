from fluid.utils.logging import (
    log_error,
    log_info,
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
    log_info("Fetching default setup.yml configuration")
    url = "https://raw.githubusercontent.com/afgalvan/fluid-setup/main/setup.yml?token=GHSAT0AAAAAABQ7JAZBW5MZUO4LXMM6B4GIYSRYOEA"
    download(url)


def load_yaml(file: str) -> Dict:
    with open(file, "r") as stream:
        try:
            return safe_load(stream)
        except YAMLError as error:
            print(error)
            log_error("Error while loading yaml file")
            exit(1)


def load_config() -> Dict:
    if exists("./setup.yml"):
        return load_yaml("./setup.yml")
    download_config()
