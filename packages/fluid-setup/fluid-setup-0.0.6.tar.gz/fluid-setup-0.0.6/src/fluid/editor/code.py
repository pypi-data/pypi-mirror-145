from fluid.utils import (
    log_info,
    log_step,
)
from os import (
    system,
)
from subprocess import (
    call,
)
from typing import (
    Dict,
)


def install_plugin(plugin: str) -> None:
    call(["code", "--force", "--install-extension", plugin])


def install_plugins(config: Dict) -> None:
    plugins_id = config["list"]
    for plugin in plugins_id:
        install_plugin(plugin)


def install_vscode() -> None:
    system(log_info("NIXPKGS_ALLOW_UNFREE=1 nix-env -i vscode"))


@log_step("Visual Studio Code")
def setup_vscode(config: Dict) -> None:
    if config["install"]:
        install_vscode()
    if config["plugins"]["setup"]:
        install_plugins(config["plugins"])
