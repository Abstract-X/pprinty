from typing import Any, Optional, TextIO


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


def _get_string(
    value: Any,
    *,
    indent: int,
    indent_level: int = 0,
    add_indent: bool = True
) -> str:
    try:
        getter = _BUILT_IN_CONTAINER_GETTERS[type(value)]
    except KeyError:
        string = repr(value)
    else:
        string = getter(value, indent, indent_level)

    if add_indent:
        string = _get_indent(indent, indent_level) + string

    return string


def _get_list_string(list_: list, indent: int, indent_level: int) -> str:
    if list_:
        lines = []
        nested_indent_level = indent_level + 1

        for i in list_:
            lines.append(
                _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

        string = "[\n" + ",\n".join(lines) + "\n" + _get_indent(indent, indent_level) + "]"
    else:
        string = "[]"

    return string


def _get_dict_string(dict_: dict, indent: int, indent_level: int) -> str:
    if dict_:
        lines = []
        nested_indent_level = indent_level + 1

        for key, value in dict_.items():
            key_string = repr(key)
            value_string = _get_string(
                value,
                indent=indent,
                indent_level=nested_indent_level,
                add_indent=False
            )
            lines.append(
                _get_indent(indent, nested_indent_level) + f"{key_string}: {value_string}"
            )

        string = "{\n" + ",\n".join(lines) + "\n" + _get_indent(indent, indent_level) + "}"
    else:
        string = "{}"

    return string


def _get_tuple_string(tuple_: tuple, indent: int, indent_level: int) -> str:
    if tuple_:
        lines = []
        nested_indent_level = indent_level + 1

        for i in tuple_:
            lines.append(
                _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

        if len(lines) == 1:
            lines = [f"{lines[0]},"]

        string = "(\n" + ",\n".join(lines) + "\n" + _get_indent(indent, indent_level) + ")"
    else:
        string = "()"

    return string


def _get_set_string(set_: set, indent: int, indent_level: int) -> str:
    if set_:
        lines = []
        nested_indent_level = indent_level + 1

        for i in set_:
            lines.append(
                _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

        string = "{\n" + ",\n".join(lines) + "\n" + _get_indent(indent, indent_level) + "}"
    else:
        string = "set()"

    return string


def _get_frozenset_string(frozenset_: frozenset, indent: int, indent_level: int) -> str:
    if frozenset_:
        lines = []
        nested_indent_level = indent_level + 1

        for i in frozenset_:
            lines.append(
                _get_string(i, indent=indent, indent_level=nested_indent_level)
            )

        string = (
            "frozenset({\n" + ",\n".join(lines) + "\n" + _get_indent(indent, indent_level) + "})"
        )
    else:
        string = "frozenset()"

    return string


_BUILT_IN_CONTAINER_GETTERS = {
    list: _get_list_string,
    dict: _get_dict_string,
    tuple: _get_tuple_string,
    set: _get_set_string,
    frozenset: _get_frozenset_string
}
