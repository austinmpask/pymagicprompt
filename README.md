# PyMagicPrompt



A powerful **one line** solution for CLI user input with absolutely zero boilerplate.



## Features

- Full lifecycle abstraction, by default looping until valid input

- Automatic terminal cleanup for subsequent prompts/answers

- Type inference & casting for answer submissions

- Customizable boolean conversion for common English words

- Built in common validators

- Support for custom validation functions

- Fully customizable prompt formatting & colors

- Customizable answer sanitization & formatting

- Obscured text for password inputs

- Options can be specified by both kwargs and `options` dict



By default, `prompt()` will work out of the box for most use cases with zero customization.



---

## Example Usage



### Basic prompt

```python
name = prompt("What is your name")
# > What is your name: John
print(name)  # 'John'
```

### Usage of built in validators

```python
age = prompt("Enter your age", numOnly=True)
# > Enter your age: 25
print(age)  # 25 (int)
```

### Custom validators

```python
def validate_range(x): 
    return 1 <= int(x) <= 10

num = prompt("Enter number 1-10", validators=[validate_range])
# > Enter number 1-10: 5
print(num)  # 5 (int)
```

### Common options for multiple inputs

```python
base = {
    "alphaOnly": True,  # Only allow letters
    "capAnswer": True,  # Capitalize the answer
    "color": "green",  # Use green color for prompt
    "suffixStr": " >> ",  # Custom suffix
    "caratStr": "! ",  # Custom carat
}

firstName = prompt("First name", options=base)
# ! First Name >> john
print(f"First name: {firstName}")  # First name: John

lastName = prompt("Last name", options=base)
# ! Last Name >> smith
print(f"Last name: {lastName}")  # Last name: Smith

```

### Custom boolean conversion

```python
proceed = prompt("Continue?", trueStrs=["sure", "ok", "yes"])
# > Continue?: ok
print(proceed)  # True (bool)

```

---

## Parameters

| Parameter          | Type                  | Default              | Description                                                                       |
| ------------------ | --------------------- | -------------------- | --------------------------------------------------------------------------------- |
| prompt             | str                   | required             | The prompt text to display to the user                                            |
| options            | PromptOptions \| None | None                 | Dictionary of options that can override default parameters                        |
| loop               | bool                  | True                 | Keep prompting until valid input is received                                      |
| capPrompt          | bool                  | True                 | Capitalize the first letter of the prompt                                         |
| titlePrompt        | bool                  | True                 | Convert prompt to title case                                                      |
| carat              | bool                  | True                 | Add a carat prefix to the prompt                                                  |
| caratStr           | str                   | "> "                 | String to use as carat                                                            |
| suffix             | bool                  | True                 | Add a suffix to the prompt                                                        |
| suffixStr          | str                   | ": "                 | String to use as suffix                                                           |
| capAnswer          | bool                  | False                | Capitalize the first letter of string answers                                     |
| titleAnswer        | bool                  | False                | Convert string answers to title case                                              |
| alphaOnly          | bool                  | False                | Only accept alphabetic input                                                      |
| numOnly            | bool                  | False                | Only accept numeric input                                                         |
| alphaNumOnly       | bool                  | False                | Only accept alphanumeric input                                                    |
| floatOnly          | bool                  | False                | Only accept floating-point numbers                                                |
| notEmpty           | bool                  | True                 | Reject empty input                                                                |
| castAnswer         | bool                  | True                 | Attempt to cast the answer to an appropriate type                                 |
| color              | str                   | ""                   | Color name for the prompt (black, red, green, yellow, blue, magenta, cyan, white) |
| isPassword         | bool                  | False                | Mask input characters                                                             |
| clearAfterResponse | bool                  | False                | Clear the prompt after receiving valid input                                      |
| trueStrs           | tuple[str, ...]       | ("true", "yes", "y") | Strings to interpret as True                                                      |
| falseStrs          | tuple[str, ...]       | ("false", "no", "n") | Strings to interpret as False                                                     |
| pwFailMsg          | str                   | "Invalid password"   | Message to display on invalid password input                                      |
| validators         | list                  | []                   | List of custom validation functions                                               |