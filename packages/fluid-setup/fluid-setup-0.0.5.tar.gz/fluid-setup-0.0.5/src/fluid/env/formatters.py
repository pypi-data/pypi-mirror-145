from subprocess import (
    call,
)
from typing import (
    Dict,
)
from fluid.utils import (
    log_step,
)


def install_makes_repo(url: str) -> None:
    call(["git", "clone", url])


def install_formatter(config: Dict) -> None:
    call(["chmod", "+x", config["src"]])
    call(["sudo", "mv", config["src"], config["target"]])


@log_step("python formatter")
def setup_python_formatter(config: Dict) -> None:
    install_makes_repo(config["makes"])
    install_formatter(config["python"])
