from fluid.editor import (
    setup_vscode,
)
from fluid.env import (
    setup_environment,
)
from fluid.utils import (
    load_config,
)


def main() -> None:
    config = load_config()
    print(config)
    # setup_vscode(config["code"])
    # setup_environment(config["environment"])
