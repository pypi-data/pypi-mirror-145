from fluid.stack.aws import (
    setup_aws,
)
from typing import (
    Dict,
)


def setup_stack(config: Dict) -> None:
    setup_aws(config["aws"])
