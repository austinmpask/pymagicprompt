from typing import Iterable, TypedDict


class PromptOptions(TypedDict, total=False):
    """Type definitions for prompt's options arg"""

    # Behavior
    loop: bool
    isPassword: bool
    clearAfterResponse: bool
    pwFailMsg: str

    # Validators
    alphaOnly: bool
    numOnly: bool
    alphaNumOnly: bool
    floatOnly: bool
    notEmpty: bool
    validators: list

    # Formatting - PROMPT
    capPrompt: bool
    titlePrompt: bool
    carat: bool
    caratStr: str
    color: str
    suffix: bool
    suffixStr: str

    # Formatting - ANSWER
    capAnswer: bool
    titleAnswer: bool
    castAnswer: bool
    trueStrs: Iterable[str]
    falseStrs: Iterable[str]


COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}
