from typing import Any

import pytest

from pprinty import pprint
from tests.stdout_context import StdoutContext


_LIST_TEST_VALUES = (
    # Empty list with indent 2
    (
        [],
        2,
        "[]\n"
    ),

    # Single element list with indent 2
    (
        [1],
        2,
        (
            "[\n"
            "  1\n"
            "]\n"
        )
    ),

    # Multiple element list with indent 2
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

    # Empty list with indent 4
    (
        [],
        4,
        "[]\n"
    ),

    # Single element list with indent 4
    (
        [1],
        4,
        (
            "[\n"
            "    1\n"
            "]\n"
        )
    ),

    # Multiple element list with indent 4
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
    )
)

_DICT_TEST_VALUES = (
    # Empty dict with indent 2
    (
        {},
        2,
        "{}\n"
    ),

    # Single element dict with indent 2
    (
        {1: 2},
        2,
        (
            "{\n"
            "  1: 2\n"
            "}\n"
        )
    ),

    # Multiple element dict with indent 2
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

    # Empty dict with indent 4
    (
        {},
        4,
        "{}\n"
    ),

    # Single element dict with indent 4
    (
        {1: 2},
        4,
        (
            "{\n"
            "    1: 2\n"
            "}\n"
        )
    ),

    # Multiple element dict with indent 4
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
    )
)

_TUPLE_TEST_VALUES = (
    # Empty tuple with indent 2
    (
        (),
        2,
        "()\n"
    ),

    # Single element tuple with indent 2
    (
        (1,),
        2,
        (
            "(\n"
            "  1,\n"
            ")\n"
        )
    ),

    # Multiple element tuple with indent 2
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

    # Empty tuple with indent 4
    (
        (),
        4,
        "()\n"
    ),

    # Single element tuple with indent 4
    (
        (1,),
        4,
        (
            "(\n"
            "    1,\n"
            ")\n"
        )
    ),

    # Multiple element tuple with indent 4
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
    )
)

_SET_TEST_VALUES = (
    # Empty set with indent 2
    (
        set(),
        2,
        "set()\n"
    ),

    # Single element set with indent 2
    (
        {1},
        2,
        (
            "{\n"
            "  1\n"
            "}\n"
        )
    ),

    # Multiple element set with indent 2
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

    # Empty set with indent 4
    (
        set(),
        4,
        "set()\n"
    ),

    # Single element set with indent 4
    (
        {1},
        4,
        (
            "{\n"
            "    1\n"
            "}\n"
        )
    ),

    # Multiple element set with indent 4
    (
        {1, 2},
        4,
        (
            "{\n"
            "    1,\n"
            "    2\n"
            "}\n"
        )
    )
)

_FROZENSET_TEST_VALUES = (
    # Empty frozenset with indent 2
    (
        frozenset(),
        2,
        "frozenset()\n"
    ),

    # Single element frozenset with indent 2
    (
        frozenset({1}),
        2,
        (
            "frozenset({\n"
            "  1\n"
            "})\n"
        )
    ),

    # Multiple element frozenset with indent 2
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

    # Empty frozenset with indent 4
    (
        frozenset(),
        4,
        "frozenset()\n"
    ),

    # Single element frozenset with indent 4
    (
        frozenset({1}),
        4,
        (
            "frozenset({\n"
            "    1\n"
            "})\n"
        )
    ),

    # Multiple element frozenset with indent 4
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
    )
)

_OTHER_TEST_VALUES = (
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


@pytest.mark.parametrize(
    ("value", "indent", "expected_result"),
    (
        _LIST_TEST_VALUES
        + _DICT_TEST_VALUES
        + _TUPLE_TEST_VALUES
        + _SET_TEST_VALUES
        + _FROZENSET_TEST_VALUES
        + _OTHER_TEST_VALUES
    )
)
def test_behavior(value: Any, indent: int, expected_result) -> None:
    stdout_context = StdoutContext()

    with stdout_context:
        pprint(value, indent=indent)

    assert stdout_context.get_value() == expected_result


@pytest.mark.parametrize(
    ("indent",),
    (
        (-1,),
        (-100,)
    )
)
def test_indent_less_than_zero(indent) -> None:
    with pytest.raises(ValueError):
        pprint(indent=indent)


@pytest.mark.parametrize(
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
def test_print_to_file(tmp_path, value: str, indent: int, expected_result: str) -> None:
    file = tmp_path / "file.txt"

    with file.open("w", encoding="UTF-8") as stream:
        pprint(value, indent=indent, file=stream)

    with file.open(encoding="UTF-8") as stream:
        content = stream.read()

    assert content == expected_result
