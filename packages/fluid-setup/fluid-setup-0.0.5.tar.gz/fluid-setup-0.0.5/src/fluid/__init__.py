from fluid.editor import (
    setup_vscode,
)
from fluid.env import (
    setup_environment,
)
from fluid.stack import (
    setup_stack,
)
from fluid.utils import (
    load_config,
)


def main() -> None:
    config = load_config()
    print(config)
    setup_environment(config["environment"])
    setup_vscode(config["code"])
    setup_stack(config["stack"])
