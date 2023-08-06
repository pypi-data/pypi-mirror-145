from subprocess import (
    call,
)
from typing import (
    Dict,
)


def git_clone(url: str) -> None:
    call(["git", "clone", url])


def sudo(function) -> None:
    def wrapper(args):
        command = function(args)
        call(["sudo"] + command)

    return wrapper
