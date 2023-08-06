from fluid.env.formatters import (
    setup_python_formatter,
)
from fluid.env.tools import (
    setup_tools,
)
from typing import (
    Dict,
)


def setup_environment(config: Dict) -> None:
    setup_tools(config["tools"])
    setup_python_formatter(config["formatters"])
