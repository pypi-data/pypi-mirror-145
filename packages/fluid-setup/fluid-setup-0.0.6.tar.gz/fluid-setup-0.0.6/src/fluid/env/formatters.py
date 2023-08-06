from fluid.utils import (
    git_clone,
    log_step,
    sudo,
)
from subprocess import (
    call,
)
from typing import (
    Dict,
)


def install_makes_repo(url: str) -> None:
    git_clone(url)


def get_formatter_src(config: str) -> str:
    return "./fluid/env/pyformat" if config == "default" else config


@sudo
def install_formatter(config: Dict) -> None:
    src = get_formatter_src(config["src"])
    call(["chmod", "+x", src])
    return ["mv", src, config["target"]]


@log_step("python formatter")
def setup_python_formatter(config: Dict) -> None:
    if not config["setup"]:
        return
    install_makes_repo(config["makes"])
    install_formatter(config["python"])
