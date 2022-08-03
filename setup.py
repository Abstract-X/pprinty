import setuptools
from pathlib import Path


_README_PATH = Path(__file__).parent / "README.md"


def get_long_description() -> str:
    with _README_PATH.open(encoding="UTF-8") as stream:
        return stream.read()


setuptools.setup(
    name="pprinty",
    version="1.1.0",
    packages=setuptools.find_packages(exclude=("tests",)),
    url="https://github.com/Abstract-X/pprinty",
    license="MIT",
    author="Abstract-X",
    author_email="abstract-x-mail@protonmail.com",
    description="A package for beautiful printing of objects.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ]
)
