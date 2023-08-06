from fluid.utils.logging import (
    log_info,
)
from subprocess import (
    call,
)


def nix_install(package: str) -> None:
    command = ["nix-env", "-i", package]
    log_info(" ".join(command))
    call(command)
