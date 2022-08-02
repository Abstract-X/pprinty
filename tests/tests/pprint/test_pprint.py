from typing import Any
from dataclasses import dataclass
from pathlib import Path

import pytest

from pprinty import pprint
from tests.stdout_context import StdoutContext


@dataclass
class FooDataclass:
    pass


@dataclass
class BarDataclass:
    a: int


@dataclass
class BazDataclass:
    a: int
    b: str


@dataclass
class BatDataclass:
    a: int
    b: str
    c: BazDataclass


BEHAVIOR_TEST_DATA = (
    ("value", "indent", "expected_result"),
    (
        # list without items and with indent 2
        (
            [],
            2,
            "[]\n"
        ),

        # list with single item and with indent 2
        (
            [1],
            2,
            (
                "[\n"
                "  1\n"
                "]\n"
            )
        ),

        # list with multiple items and with indent 2
        (
            [1, 2],
            2,
            (
                "[\n"
                "  1,\n"
                "  2\n"
                "]\n"
            )
        ),

        # Nested list with indent 2
        (
            [1, [2, 3]],
            2,
            (
                "[\n"
                "  1,\n"
                "  [\n"
                "    2,\n"
                "    3\n"
                "  ]\n"
                "]\n"
            )
        ),

        # list without items and with indent 4
        (
            [],
            4,
            "[]\n"
        ),

        # list with single item and with indent 4
        (
            [1],
            4,
            (
                "[\n"
                "    1\n"
                "]\n"
            )
        ),

        # list with multiple items and with indent 4
        (
            [1, 2],
            4,
            (
                "[\n"
                "    1,\n"
                "    2\n"
                "]\n"
            )
        ),

        # Nested list with indent 4
        (
            [1, [2, 3]],
            4,
            (
                "[\n"
                "    1,\n"
                "    [\n"
                "        2,\n"
                "        3\n"
                "    ]\n"
                "]\n"
            )
        ),

        # dict without items and with indent 2
        (
            {},
            2,
            "{}\n"
        ),

        # dict with single item and with indent 2
        (
            {1: 2},
            2,
            (
                "{\n"
                "  1: 2\n"
                "}\n"
            )
        ),

        # dict with multiple items and with indent 2
        (
            {1: 2, 3: 4},
            2,
            (
                "{\n"
                "  1: 2,\n"
                "  3: 4\n"
                "}\n"
            )
        ),

        # Nested dict with indent 2
        (
            {1: {2: 3}},
            2,
            (
                "{\n"
                "  1: {\n"
                "    2: 3\n"
                "  }\n"
                "}\n"
            )
        ),

        # dict without items and with indent 4
        (
            {},
            4,
            "{}\n"
        ),

        # dict with single item and with indent 4
        (
            {1: 2},
            4,
            (
                "{\n"
                "    1: 2\n"
                "}\n"
            )
        ),

        # dict with multiple items and with indent 4
        (
            {1: 2, 3: 4},
            4,
            (
                "{\n"
                "    1: 2,\n"
                "    3: 4\n"
                "}\n"
            )
        ),

        # Nested dict with indent 4
        (
            {1: {2: 3}},
            4,
            (
                "{\n"
                "    1: {\n"
                "        2: 3\n"
                "    }\n"
                "}\n"
            )
        ),

        # tuple without items and with indent 2
        (
            (),
            2,
            "()\n"
        ),

        # tuple with single item and with indent 2
        (
            (1,),
            2,
            (
                "(\n"
                "  1,\n"
                ")\n"
            )
        ),

        # tuple with multiple items and with indent 2
        (
            (1, 2),
            2,
            (
                "(\n"
                "  1,\n"
                "  2\n"
                ")\n"
            )
        ),

        # Nested tuple with indent 2
        (
            (1, (2, 3)),
            2,
            (
                "(\n"
                "  1,\n"
                "  (\n"
                "    2,\n"
                "    3\n"
                "  )\n"
                ")\n"
            )
        ),

        # tuple without items and with indent 4
        (
            (),
            4,
            "()\n"
        ),

        # tuple with single item and with indent 4
        (
            (1,),
            4,
            (
                "(\n"
                "    1,\n"
                ")\n"
            )
        ),

        # tuple with multiple items and with indent 4
        (
            (1, 2),
            4,
            (
                "(\n"
                "    1,\n"
                "    2\n"
                ")\n"
            )
        ),

        # Nested tuple with indent 4
        (
            (1, (2, 3)),
            4,
            (
                "(\n"
                "    1,\n"
                "    (\n"
                "        2,\n"
                "        3\n"
                "    )\n"
                ")\n"
            )
        ),

        # set without items and with indent 2
        (
            set(),
            2,
            "set()\n"
        ),

        # set with single item and with indent 2
        (
            {1},
            2,
            (
                "{\n"
                "  1\n"
                "}\n"
            )
        ),

        # set with multiple items and with indent 2
        (
            {1, 2},
            2,
            (
                "{\n"
                "  1,\n"
                "  2\n"
                "}\n"
            )
        ),

        # set without items and with indent 4
        (
            set(),
            4,
            "set()\n"
        ),

        # set with single item and with indent 4
        (
            {1},
            4,
            (
                "{\n"
                "    1\n"
                "}\n"
            )
        ),

        # set with multiple items and with indent 4
        (
            {1, 2},
            4,
            (
                "{\n"
                "    1,\n"
                "    2\n"
                "}\n"
            )
        ),

        # frozenset without items and with indent 2
        (
            frozenset(),
            2,
            "frozenset()\n"
        ),

        # frozenset with single item and with indent 2
        (
            frozenset({1}),
            2,
            (
                "frozenset({\n"
                "  1\n"
                "})\n"
            )
        ),

        # frozenset with multiple items and with indent 2
        (
            frozenset({1, 2}),
            2,
            (
                "frozenset({\n"
                "  1,\n"
                "  2\n"
                "})\n"
            )
        ),

        # Nested frozenset with indent 2
        (
            frozenset({1, frozenset({2, 3})}),
            2,
            (
                "frozenset({\n"
                "  1,\n"
                "  frozenset({\n"
                "    2,\n"
                "    3\n"
                "  })\n"
                "})\n"
            )
        ),

        # frozenset without items and with indent 4
        (
            frozenset(),
            4,
            "frozenset()\n"
        ),

        # frozenset with single item and with indent 4
        (
            frozenset({1}),
            4,
            (
                "frozenset({\n"
                "    1\n"
                "})\n"
            )
        ),

        # frozenset with multiple items and with indent 4
        (
            frozenset({1, 2}),
            4,
            (
                "frozenset({\n"
                "    1,\n"
                "    2\n"
                "})\n"
            )
        ),

        # Nested frozenset with indent 4
        (
            frozenset({1, frozenset({2, 3})}),
            4,
            (
                "frozenset({\n"
                "    1,\n"
                "    frozenset({\n"
                "        2,\n"
                "        3\n"
                "    })\n"
                "})\n"
            )
        ),

        # Dataclass without fields and with indent 2
        (
            FooDataclass(),
            2,
            "FooDataclass()\n"
        ),

        # Dataclass with single field and with indent 2
        (
            BarDataclass(12345),
            2,
            (
                "BarDataclass(\n"
                "  a=12345\n"
                ")\n"
            )
        ),
        
        # Dataclass with multiple fields and with indent 2
        (
            BazDataclass(12345, "field_value"),
            2,
            (
                "BazDataclass(\n"
                "  a=12345,\n"
                "  b='field_value'\n"
                ")\n"
            )
        ),

        # Nested dataclass with indent 2
        (
            BatDataclass(12345, "bat_field_value", BazDataclass(54321, "baz_field_value")),
            2,
            "BatDataclass(\n"
            "  a=12345,\n"
            "  b='bat_field_value',\n"
            "  c=BazDataclass(\n"
            "    a=54321,\n"
            "    b='baz_field_value'\n"
            "  )\n"
            ")\n"
        ),

        # Dataclass without fields and with indent 4
        (
            FooDataclass(),
            4,
            "FooDataclass()\n"
        ),

        # Dataclass with single field and with indent 4
        (
            BarDataclass(12345),
            4,
            (
                "BarDataclass(\n"
                "    a=12345\n"
                ")\n"
            )
        ),

        # Dataclass with multiple fields and with indent 4
        (
            BazDataclass(12345, "field_value"),
            4,
            (
                "BazDataclass(\n"
                "    a=12345,\n"
                "    b='field_value'\n"
                ")\n"
            )
        ),

        # Nested dataclass with indent 4
        (
            BatDataclass(12345, "bat_field_value", BazDataclass(54321, "baz_field_value")),
            4,
            "BatDataclass(\n"
            "    a=12345,\n"
            "    b='bat_field_value',\n"
            "    c=BazDataclass(\n"
            "        a=54321,\n"
            "        b='baz_field_value'\n"
            "    )\n"
            ")\n"
        ),

        # str
        (
            "string",
            2,
            "'string'\n"
        ),
        (
            "string",
            4,
            "'string'\n"
        ),

        # int
        (
            12345,
            2,
            "12345\n"
        ),
        (
            12345,
            4,
            "12345\n"
        ),

        # float
        (
            123.45,
            2,
            "123.45\n"
        ),
        (
            123.45,
            4,
            "123.45\n"
        ),

        # bool
        (
            True,
            2,
            "True\n"
        ),
        (
            True,
            4,
            "True\n"
        ),
        (
            False,
            2,
            "False\n"
        ),
        (
            False,
            4,
            "False\n"
        ),

        # None
        (
            None,
            2,
            "None\n"
        ),
        (
            None,
            4,
            "None\n"
        )
    )
)
INDENT_LESS_THAN_ZERO_TEST_DATA = (
    ("indent",),
    (
        (-1,),
        (-100,)
    )
)
PRINT_TO_FILE_TEST_DATA = (
    ("value", "indent", "expected_result"),
    (
        (
            "foobar",
            4,
            "'foobar'\n"
        ),
        (
            {1: {2: 3}},
            2,
            (
                "{\n"
                "  1: {\n"
                "    2: 3\n"
                "  }\n"
                "}\n"
            )
        ),
        (
            {1: {2: 3}},
            4,
            (
                "{\n"
                "    1: {\n"
                "        2: 3\n"
                "    }\n"
                "}\n"
            )
        )
    )
)


@pytest.mark.parametrize(*BEHAVIOR_TEST_DATA)
def test_behavior(value: Any, indent: int, expected_result: str) -> None:
    stdout_context = StdoutContext()

    with stdout_context:
        pprint(value, indent=indent)

    assert stdout_context.get_value() == expected_result


@pytest.mark.parametrize(*INDENT_LESS_THAN_ZERO_TEST_DATA)
def test_indent_less_than_zero(indent: int) -> None:
    with pytest.raises(ValueError):
        pprint(indent=indent)


@pytest.mark.parametrize(*PRINT_TO_FILE_TEST_DATA)
def test_print_to_file(tmp_path: Path, value: str, indent: int, expected_result: str) -> None:
    file = tmp_path / "file.txt"

    with file.open("w", encoding="UTF-8") as stream:
        pprint(value, indent=indent, file=stream)

    with file.open(encoding="UTF-8") as stream:
        content = stream.read()

    assert content == expected_result
