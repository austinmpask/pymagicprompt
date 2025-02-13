from getpass import getpass

from config import COLORS, PromptOptions
from utils import clrLn, inferType, validate


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
    pwFailMsg="Invalid password",
    validators=[],
):

    # Create a dict out of kwarg options
    dOptions: PromptOptions = {
        k: v for k, v in locals().items() if k not in ("prompt", "options")
    }

    # If user supplied options via dict, update with those values instead
    if options:
        dOptions.update(options)

    # Map prompt formatting options to functions
    promptFormatters = [
        ("capPrompt", str.capitalize),
        ("titlePrompt", str.title),
        ("carat", lambda x: f"{caratStr}{x}"),
        ("suffix", lambda x: f"{x}{suffixStr}"),
        (
            "color",
            lambda x: f"{COLORS.get(color, COLORS["reset"])}{x}{COLORS["reset"]}",
        ),
    ]

    # Format prompt based on selected formatting options
    for o, fn in promptFormatters:
        if dOptions[o]:
            prompt = fn(prompt)

    # Pose prompt to user
    while True:

        # Obscure text if input is for password
        if dOptions["isPassword"]:
            a = getpass(prompt)
        else:
            a = input(prompt)

        # Exit the loop if validations pass, or if looping is disabled
        if validate(a, dOptions) or not dOptions["loop"]:

            # Clear line following end of lifecycle if chosen
            if dOptions["clearAfterResponse"]:
                clrLn()
            break

        # Clear line if prompt will be posed again
        if dOptions["isPassword"]:
            print(pwFailMsg)
        else:
            clrLn()

    # Type cast answer
    if dOptions["castAnswer"]:
        a = inferType(a, trueStrs, falseStrs)

    # Format answer if it is still a string
    if isinstance(a, str):

        # Map answer formatting options to functions
        ansFormatters = [
            ("capAnswer", str.capitalize),
            ("titleAnswer", str.title),
        ]

        # Format according to choices
        for o, fn in ansFormatters:
            if dOptions[o]:
                a = fn(a)

    return a
