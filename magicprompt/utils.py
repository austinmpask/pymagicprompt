import sys
from typing import Iterable


def isfloat(string: str) -> bool:
    """Determine if string should be cast to float, given it was not considered an int

    Args:
        string (str): User's input to analyze

    Returns:
        bool: Indicates if type inference should be bool for user's input
    """
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


def inferType(
    a: str, trueStrs: Iterable[str], falseStrs: Iterable[str]
) -> bool | int | float | str | None:
    """Casts the user's input str to the most appropriate type

    Args:
        a (str): User's input/answer
        trueStrs (Iterable[str]): Iterable containing any strings which should be synonymous to "True"
        falseStrs (Iterable[str]): Iterable containing any strings which should be synonymous to "False"

    Returns:
        bool | int | float | str | None: User's input cast to appropriate type
    """
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


def validate(a: str, options: dict) -> bool:
    """Iterates through any validations which have been selected in prompt options dict

    Args:
        a (str): User's input/answer
        options (dict): Options dict from prompt

    Returns:
        bool: Returns True when all validations pass, False otherwise
    """

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

    # Perform custom validations
    if len(options["validators"]):
        for v in options["validators"]:
            if not v(a):
                return False

    # Validations passed
    return True
