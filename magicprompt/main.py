from getpass import getpass

from magicprompt.config import COLORS, PromptOptions
from magicprompt.utils import clrLn, inferType, validate


def prompt(
    prompt: str,
    options: PromptOptions | None = None,
    *,
    loop: bool = True,
    capPrompt: bool = True,
    titlePrompt: bool = False,
    carat: bool = True,
    caratStr: str = "> ",
    suffix: bool = True,
    suffixStr: str = ": ",
    capAnswer: bool = False,
    titleAnswer: bool = False,
    alphaOnly: bool = False,
    numOnly: bool = False,
    alphaNumOnly: bool = False,
    floatOnly: bool = False,
    notEmpty: bool = True,
    castAnswer: bool = True,
    color: str = "",
    isPassword: bool = False,
    clearAfterResponse: bool = False,
    trueStrs: tuple[str, ...] = ("true", "yes", "y"),
    falseStrs: tuple[str, ...] = ("false", "no", "n"),
    pwFailMsg: str = "Invalid password",
    validators: list = [],
) -> str | int | float | bool | None:
    """
    Prompts the user for input with extensive formatting and validation options.

    This function provides a flexible way to collect user input with support for:
    - Input validation and type casting
    - Text formatting for both prompts and answers
    - Password input masking
    - Boolean conversion
    - Custom validation rules
    - Terminal display options

    Args:
        prompt (str): The prompt text to display to the user
        options (PromptOptions | None): A dictionary of options that can override the default parameters
        loop (bool): Whether to keep prompting until valid input is received
        capPrompt (bool): Capitalize the first letter of the prompt
        titlePrompt (bool): Convert prompt to title case
        carat (bool): Add a carat prefix to the prompt
        caratStr (str): The string to use as carat (default: "> ")
        suffix (bool): Add a suffix to the prompt
        suffixStr (str): The string to use as suffix (default: ": ")
        capAnswer (bool): Capitalize the first letter of string answers
        titleAnswer (bool): Convert string answers to title case
        alphaOnly (bool): Only accept alphabetic input
        numOnly (bool): Only accept numeric input
        alphaNumOnly (bool): Only accept alphanumeric input
        floatOnly (bool): Only accept floating-point numbers
        notEmpty (bool): Reject empty input
        castAnswer (bool): Attempt to cast the answer to an appropriate type
        color (str): Color name for the prompt (must be defined in COLORS)
        isPassword (bool): Mask input characters (for passwords)
        clearAfterResponse (bool): Clear the prompt after receiving valid input
        trueStrs (tuple[str, ...]): Strings to interpret as True
        falseStrs (tuple[str, ...]): Strings to interpret as False
        pwFailMsg (str): Message to display on invalid password input
        validators (list): List of custom validation functions

    Returns:
        Union[str, int, float, bool, None]: The processed user input. The type depends on:
            - str: If castAnswer is False or the input doesn't match other types
            - int: If the input is a valid integer and castAnswer is True
            - float: If the input is a valid float and castAnswer is True
            - bool: If the input matches trueStrs or falseStrs and castAnswer is True
            - None: If the input is empty and notEmpty is False

    Examples:
        Basic prompt:
        >>> name = prompt("What is your name")
        > What is your name: John
        >>> print(name)
        'John'

        Number input with validation:
        >>> age = prompt("Enter your age", numOnly=True, castAnswer=True)
        > Enter your age: 25
        >>> print(age)
        25

        Password input:
        >>> pwd = prompt("Enter password", isPassword=True)
        > Enter password: ****

        Boolean input:
        >>> proceed = prompt("Continue?", castAnswer=True)
        > Continue?: yes
        >>> print(proceed)
        True

        Custom validation:
        >>> def validate_range(x): return 1 <= int(x) <= 10
        >>> num = prompt("Enter number 1-10", validators=[validate_range])
        > Enter number 1-10: 5
        >>> print(num)
        '5'
    """

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
