import sys
from getpass import getpass
from typing import Iterable, TypedDict


# Define option types for autocomplete etc.
class PromptOptions(TypedDict, total=False):

    # Behavior
    loop: bool
    isPassword: bool
    clearAfterResponse: bool

    # Validators
    alphaOnly: bool
    numOnly: bool
    alphaNumOnly: bool
    floatOnly: bool
    notEmpty: bool

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


def isfloat(string: str) -> bool:

    # Check for decimal
    if "." not in string:
        return False

    # Try to cast
    try:
        float(string)
        return True
    except ValueError:
        return False


def clrLn():
    """Clears one line from std. out"""
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")  # Clear to end of line


def validate(a: str, options: dict) -> bool:

    # Map options to validations
    validators = [
        ("alphaOnly", str.isalpha),
        ("numOnly", str.isnumeric),
        ("floatOnly", isfloat),
        ("alphaNumOnly", str.isalnum),
        ("notEmpty", lambda x: x != ""),
    ]

    # Return false if any validator did not pass
    for o, validator in validators:
        if options[o]:
            if not validator(a):
                return False

    # Validations passed
    return True


def inferType(
    a: str, trueStrs: Iterable[str], falseStrs: Iterable[str]
) -> bool | int | float | str | None:
    if a.isnumeric():
        return int(a)

    if isfloat(a):
        return float(a)

    if a.lower() in trueStrs:
        return True

    if a.lower() in falseStrs:
        return False

    if a == "":
        return None

    return a


def prompt(
    prompt: str,
    options: PromptOptions | None = None,
    *,
    loop=True,
    capPrompt=True,
    titlePrompt=True,
    carat=True,
    caratStr="> ",
    suffix=True,
    suffixStr=": ",
    capAnswer=False,
    titleAnswer=False,
    alphaOnly=False,
    numOnly=False,
    alphaNumOnly=False,
    floatOnly=False,
    notEmpty=True,
    castAnswer=True,
    color="",
    isPassword=False,
    clearAfterResponse=False,
    trueStrs=("true", "yes", "y"),
    falseStrs=("false", "no", "n"),
):

    # Forward option kwargs
    dOptions: PromptOptions = {
        k: v for k, v in locals().items() if k not in ("prompt", "options")
    }

    # Update from options obj if present
    if options:
        dOptions.update(options)

    colors = {
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

    # Map prompt formatting options to functions
    promptFormatters = [
        ("capPrompt", str.capitalize),
        ("titlePrompt", str.title),
        ("carat", lambda x: f"{caratStr}{x}"),
        ("suffix", lambda x: f"{x}{suffixStr}"),
        (
            "color",
            lambda x: f"{colors.get(color, colors["reset"])}{x}{colors["reset"]}",
        ),
    ]

    # Format prompt
    for o, fn in promptFormatters:
        if dOptions[o]:
            prompt = fn(prompt)

    # Pose prompt
    while True:
        if dOptions["isPassword"]:
            a = getpass(prompt)
        else:
            a = input(prompt)

        if validate(a, dOptions) or not dOptions["loop"]:
            if dOptions["clearAfterResponse"]:
                clrLn()
            break
        # Clear line if prompt will be re-posed
        if dOptions["isPassword"]:
            print("Invalid password")
        else:
            clrLn()

    # Map answer formatting options to functions
    ansFormatters = [
        ("capAnswer", str.capitalize),
        ("titleAnswer", str.title),
    ]

    # Type cast answer
    if dOptions["castAnswer"]:
        a = inferType(a, trueStrs, falseStrs)

    # Format answer if it is still a string
    if isinstance(a, str):
        for o, fn in ansFormatters:
            if dOptions[o]:
                a = fn(a)

    return a


ans = prompt("hello", alphaOnly=True)

print(ans)
