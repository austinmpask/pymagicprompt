import pytest

from magicprompt import inferType, isfloat, validate


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1.0, True),
        (0.0, True),
        (1, False),
        ("", False),
        (None, False),
        (" ", False),
        ("a", False),
    ],
)
def test_isfloat(test_input, expected):
    assert isfloat(str(test_input)) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1.0, float),
        (0.0, float),
        (1, int),
        (" ", str),
        ("a", str),
    ],
)
def test_inferType(test_input, expected):
    assert isinstance(inferType(str(test_input), ["y"], ["n"]), expected)


def test_inferTypeNone():
    assert inferType("", ["y"], ["n"]) is None


def test_validate_defaults():
    """Test with no validation options enabled"""
    options = {
        "alphaOnly": False,
        "numOnly": False,
        "floatOnly": False,
        "alphaNumOnly": False,
        "notEmpty": False,
        "validators": [],
    }
    assert validate("any input", options) == True


@pytest.mark.parametrize(
    "test_input,validation,expected",
    [
        ("abc", "alphaOnly", True),
        ("abc123", "alphaOnly", False),
        ("123", "numOnly", True),
        ("abc123", "numOnly", False),
        ("1.23", "floatOnly", True),
        ("abc", "floatOnly", False),
        ("abc123", "alphaNumOnly", True),
        ("abc!123", "alphaNumOnly", False),
        ("something", "notEmpty", True),
        ("", "notEmpty", False),
    ],
)
def test_single_validations(test_input, validation, expected):
    """Test each validation type individually"""
    options = {
        "alphaOnly": False,
        "numOnly": False,
        "floatOnly": False,
        "alphaNumOnly": False,
        "notEmpty": False,
        "validators": [],
    }
    options[validation] = True
    assert validate(test_input, options) == expected


def test_multiple_validations():
    """Test multiple validations at once"""
    options = {
        "alphaOnly": True,
        "notEmpty": True,
        "numOnly": False,
        "floatOnly": False,
        "alphaNumOnly": False,
        "validators": [],
    }
    assert validate("abc", options) == True
    assert validate("123", options) == False
    assert validate("", options) == False


def test_custom_validators():
    """Test custom validation functions"""

    def is_short(s):
        return len(s) < 5

    def starts_with_a(s):
        return s.startswith("a")

    options = {
        "alphaOnly": False,
        "numOnly": False,
        "floatOnly": False,
        "alphaNumOnly": False,
        "notEmpty": False,
        "validators": [is_short, starts_with_a],
    }

    assert validate("abc", options) == True
    assert validate("abcdef", options) == False
    assert validate("xyz", options) == False


def test_combined_built_in_and_custom():
    """Test combination of built-in and custom validators"""

    def is_short(s):
        return len(s) < 5

    options = {
        "alphaOnly": True,
        "numOnly": False,
        "floatOnly": False,
        "alphaNumOnly": False,
        "notEmpty": True,
        "validators": [is_short],
    }

    assert validate("abc", options) == True
    assert validate("abcd", options) == True
    assert validate("abcde", options) == False
    assert validate("abc123", options) == False
    assert validate("", options) == False


@pytest.mark.parametrize(
    "options,test_input,expected",
    [
        ({"alphaOnly": True, "numOnly": True, "validators": []}, "abc123", False),
        ({"alphaOnly": True, "alphaNumOnly": True, "validators": []}, "abc123", False),
        (
            {"alphaOnly": False, "floatOnly": True, "numOnly": True, "validators": []},
            "1.23",
            False,
        ),
    ],
)
def test_conflicting_validations(options, test_input, expected):
    """Test behavior with conflicting validation rules"""
    # Fill in required options
    options.update(
        {
            "floatOnly": options.get("floatOnly", False),
            "alphaNumOnly": options.get("alphaNumOnly", False),
            "notEmpty": options.get("notEmpty", False),
        }
    )
    assert validate(test_input, options) == expected
