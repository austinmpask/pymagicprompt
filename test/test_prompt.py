from unittest.mock import patch

import pytest

from magicprompt import prompt


@pytest.fixture
def basic_options():
    return {
        "loop": True,
        "capPrompt": False,
        "titlePrompt": False,
        "carat": False,
        "suffix": False,
        "capAnswer": False,
        "titleAnswer": False,
        "alphaOnly": False,
        "numOnly": False,
        "alphaNumOnly": False,
        "floatOnly": False,
        "notEmpty": False,
        "castAnswer": True,
        "color": "",
        "isPassword": False,
        "clearAfterResponse": False,
        "validators": [],
    }


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("hello", "hello"),
        ("123", 123),
        ("12.34", 12.34),
        ("true", True),
        ("yes", True),
        ("false", False),
    ],
)
def test_basic_prompt(test_input, expected):
    with patch("builtins.input", return_value=test_input):
        result = prompt("Test prompt", castAnswer=True)
        assert result == expected


@pytest.mark.parametrize(
    "options,test_input,expected",
    [
        ({"capAnswer": True}, "hello world", "Hello world"),
        ({"titleAnswer": True}, "hello world", "Hello World"),
        ({"capAnswer": True, "titleAnswer": True}, "hello world", "Hello World"),
        ({"castAnswer": False}, "123", "123"),  # Don't cast to int
    ],
)
def test_answer_formatting(options, test_input, expected):
    with patch("builtins.input", return_value=test_input):
        result = prompt("Test prompt", options=options)
        assert result == expected


def test_validation_loop():

    input_values = ["123", "abc"]
    input_mock = patch("builtins.input", side_effect=input_values)

    with input_mock:
        result = prompt("Test", alphaOnly=True)
        assert result == "abc"


def test_custom_validators():
    def is_short(s):
        return len(s) < 5

    with patch("builtins.input", side_effect=["toolong", "ok"]):
        result = prompt("Test", validators=[is_short])
        assert result == "ok"


@pytest.mark.parametrize(
    "test_input,true_strs,false_strs,expected",
    [
        ("yes", ("yes", "y"), ("no", "n"), True),
        ("n", ("yes", "y"), ("no", "n"), False),
        ("custom", ("custom",), ("not",), True),
    ],
)
def test_boolean_casting(test_input, true_strs, false_strs, expected):
    with patch("builtins.input", return_value=test_input):
        result = prompt("Test", trueStrs=true_strs, falseStrs=false_strs)
        assert result == expected


def test_combined_validations():
    options = {
        "alphaOnly": True,
        "notEmpty": True,
        "validators": [lambda x: len(x) < 5],
    }

    with patch("builtins.input", side_effect=["123", "", "toolong", "abc"]):
        result = prompt("Test", options=options)
        assert result == "abc"


def test_no_loop():
    with patch("builtins.input", return_value="123"):

        result = prompt("Test", loop=False, alphaOnly=True)
        assert result == 123
