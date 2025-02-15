from setuptools import find_packages, setup

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="magicprompt",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/austinmpask/pymagicprompt",
    long_description=description,
    long_description_content_type="text/markdown",
    description="A powerful one line solution for collecting CLI user input with absolutely zero boilerplate",
)
