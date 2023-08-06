from fluid.utils import (
    log_step,
    nix_install,
)
from fluid.utils.logging import (
    log_info,
)
from subprocess import (
    call,
)
from typing import (
    Dict,
    List,
)


def get_tool_names(config: Dict) -> List[str]:
    return config["list"]


@log_step("environment tools")
def setup_tools(config: Dict) -> None:
    if not config["setup"]:
        return
    tools = get_tool_names(config)
    for tool in tools:
        nix_install(tool)
