from os import (
    system,
)
from subprocess import (
    call,
)
from typing import (
    Dict,
    List,
)
from fluid.utils import (
    log_step,
)


def get_plugins_id(config: Dict) -> List[str]:
    return config["plugins"]["list"]


def install_plugin(plugin: str) -> None:
    call(["code", "--force", "--install-extension", plugin])


def install_plugins(config: Dict) -> None:
    plugins_id = get_plugins_id(config)
    for plugin in plugins_id:
        install_plugin(plugin)


def install_vscode() -> None:
    system("NIXPKGS_ALLOW_UNFREE=1 nix-env -i vscode")


@log_step("Visual Studio Code")
def setup_vscode(config: Dict) -> None:
    install_vscode()
    if config["plugins"]["install"]:
        install_plugins(config)
