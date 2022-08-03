from typing import Any, Optional, TextIO, List
import dataclasses


_SENTINEL = object()


def pprint(value: Any = _SENTINEL, *, indent: int = 4, file: Optional[TextIO] = None) -> None:
    """Print a decomposed value to sys.stdout or a file.

    :param value: A value to print.
    :param indent: A number of spaces before a string. Used to decompose containers.
    :param file: A file-like object to print to a file.
    :raises ValueError: If an indent is less than zero.
    """
    if indent < 0:
        raise ValueError("Indent cannot be less than zero!")

    if value is not _SENTINEL:
        print(
            _get_string(value, indent=indent),
            file=file
        )
    else:
        print(file=file)


def _get_indent(value: int, level: int) -> str:
    return " " * value * level


def _get_total_string(
    start_string: str,
    lines: List[str],
    end_string: str,
    indent: int,
    indent_level: int,
    no_line_string: Optional[str] = None
) -> str:
    if lines:
        return (
            start_string
            + "\n"
            + ",\n".join(lines)
            + "\n"
            + _get_indent(indent, indent_level)
            + end_string
        )
    elif no_line_string is not None:
        return no_line_string

    return f"{start_string}{end_string}"


def _get_string(
    value: Any,
    *,
    indent: int,
    indent_level: int = 0
) -> str:
    type_ = type(value)

    if type_ in _BUILT_IN_CONTAINER_GETTERS:
        getter = _BUILT_IN_CONTAINER_GETTERS[type_]
        string = getter(value, indent, indent_level)
    elif dataclasses.is_dataclass(type_):
        string = _get_dataclass_string(value, indent, indent_level)
    else:
        string = repr(value)

    return string


def _get_list_string(object_: list, indent: int, indent_level: int) -> str:
    lines = []

    if object_:
        nested_indent_level = indent_level + 1

        for i in object_:
            lines.append(
                _get_indent(indent, nested_indent_level)
                + _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

    return _get_total_string(
        start_string="[",
        lines=lines,
        end_string="]",
        indent=indent,
        indent_level=indent_level
    )


def _get_dict_string(object_: dict, indent: int, indent_level: int) -> str:
    lines = []

    if object_:
        nested_indent_level = indent_level + 1

        for key, value in object_.items():
            key_string = repr(key)
            value_string = _get_string(value, indent=indent, indent_level=nested_indent_level)
            lines.append(
                _get_indent(indent, nested_indent_level) + f"{key_string}: {value_string}"
            )

    return _get_total_string(
        start_string="{",
        lines=lines,
        end_string="}",
        indent=indent,
        indent_level=indent_level
    )


def _get_tuple_string(object_: tuple, indent: int, indent_level: int) -> str:
    lines = []

    if object_:
        nested_indent_level = indent_level + 1

        for i in object_:
            lines.append(
                _get_indent(indent, nested_indent_level)
                + _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

        if len(lines) == 1:
            lines = [f"{lines[0]},"]

    return _get_total_string(
        start_string="(",
        lines=lines,
        end_string=")",
        indent=indent,
        indent_level=indent_level
    )


def _get_set_string(object_: set, indent: int, indent_level: int) -> str:
    lines = []

    if object_:
        nested_indent_level = indent_level + 1

        for i in object_:
            lines.append(
                _get_indent(indent, nested_indent_level)
                + _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

    return _get_total_string(
        start_string="{",
        lines=lines,
        end_string="}",
        indent=indent,
        indent_level=indent_level,
        no_line_string="set()"
    )


def _get_frozenset_string(object_: frozenset, indent: int, indent_level: int) -> str:
    lines = []

    if object_:
        nested_indent_level = indent_level + 1

        for i in object_:
            lines.append(
                _get_indent(indent, nested_indent_level)
                + _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

    return _get_total_string(
        start_string="frozenset({",
        lines=lines,
        end_string="})",
        indent=indent,
        indent_level=indent_level,
        no_line_string="frozenset()"
    )


def _get_dataclass_string(object_: object, indent: int, indent_level: int) -> str:
    lines = []
    nested_indent_level = indent_level + 1

    if hasattr(object_, "__slots__"):
        object_data = {
            i: getattr(object_, i)
            for i in object_.__slots__
            if hasattr(object_, i)
        }
    else:
        object_data = vars(object_)

    for name, value in object_data.items():
        value_string = _get_string(value, indent=indent, indent_level=nested_indent_level)
        lines.append(
            _get_indent(indent, nested_indent_level) + f"{name}={value_string}"
        )

    return _get_total_string(
        start_string=f"{type(object_).__name__}(",
        lines=lines,
        end_string=")",
        indent=indent,
        indent_level=indent_level,
    )


_BUILT_IN_CONTAINER_GETTERS = {
    list: _get_list_string,
    dict: _get_dict_string,
    tuple: _get_tuple_string,
    set: _get_set_string,
    frozenset: _get_frozenset_string
}
