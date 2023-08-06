from loguru import (
    logger,
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


def get_tool_names(config: Dict) -> List[str]:
    return config["list"]


def install_tool(tool: str) -> None:
    command = ["nix-env", "-i", tool]
    logger.info(" ".join(command))
    call(command)


@log_step("environment tools")
def setup_tools(config: Dict) -> None:
    if not config["install"]:
        return
    tools = get_tool_names(config)
    for tool in tools:
        install_tool(tool)
