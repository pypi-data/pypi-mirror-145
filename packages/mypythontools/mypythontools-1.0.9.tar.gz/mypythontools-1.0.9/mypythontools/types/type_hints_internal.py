"""Module with functions for 'type_hints' subpackage."""

from __future__ import annotations
import sys

# Import can be used in eval
from typing import (
    Any,
    Callable,
    Union,
    List,
    Dict,
    Tuple,
    Sequence,
    Iterable,
)  # pylint: disable=unused-import

from typing_extensions import Literal, get_origin, get_args, get_type_hints

from typeguard import typechecked  # , check_type

import mylogging


def typechecked_compatible(function):
    """Turns off type checking for old incompatible python versions.

    Mainly for new syntax like list[str] which raise TypeError.
    """

    # def decorator(func):
    #     if sys.version_info.minor < 9:
    #         return func
    #     return typechecked(func)

    if sys.version_info.minor < 9:
        return function
    return typechecked(function)


def get_return_type_hints(func: Callable) -> Any:
    """Return function return types.

    This is because `get_type_hints` result in error for some types in older
    versions of python and also that `__annotations__` contains only string, not types.

    Note:
        Sometimes it may use eval as literal_eval cannot use users globals so types like pd.DataFrame would
        fail. Therefore do not use it for evaluating types of users input for sake of security.

    Args:
        func (Callable): Function with type hints.

    Returns:
        Any: Type of return.

    Example:
        >>> # You can use Union as well as Literal
        >>> def union_return() -> int | float:
        ...     return 1
        >>> inferred_type = get_return_type_hints(union_return)
        >>> 'int' in str(inferred_type) and 'float' in str(inferred_type)
        True
        >>> def literal_return() -> Literal[1, 2, 3]:
        ...     return 1
        >>> inferred_type = get_return_type_hints(literal_return)
        >>> 'Literal' in str(inferred_type)
        True
    """
    if isinstance(func, staticmethod):
        func = func.__func__

    try:
        types = get_type_hints(func).get("return")
    except Exception:
        types = func.__annotations__.get("return")

    if isinstance(types, str) and "Union" in types:
        types = eval(types, func.__globals__)

    # If Union operator |, e.g. int | str - get_type_hints() result in TypeError
    # Convert it to Union
    elif isinstance(types, str) and "|" in types:
        str_types = [i.strip() for i in types.split("|")]
        for i, j in enumerate(str_types):
            for k in ["list", "dict", "tuple"]:
                if k in j:
                    str_types[i] = j.replace(k, k.capitalize())
        try:
            evaluated_types = [eval(i, {**globals(), **func.__globals__}) for i in str_types]
        except Exception:
            raise RuntimeError("Evaluating of function return type failed. Try it on python 3.9+.")

        types = Union[evaluated_types[0], evaluated_types[1]]  # type: ignore

        if len(evaluated_types) > 2:
            for i in evaluated_types[2:]:
                types = Union[types, i]

    return types


class ValidationError(TypeError):
    """To know that error is because of bad config type and not some TypeError from the inside."""

    pass


# def validate(value, allowed_type: Any, name: str) -> None:
#     """Type validation. It also works for Union and validate Literal values.

#     Instead of typeguard validation, it define just subset of types, but is simplier
#     and needs no extra import, therefore can be faster.

#     Args:
#         value (Any): Value that will be validated.
#         allowed_type (Any, optional): For example int, str or list. It can be also Union
#             or Literal. If Literal, validated value has to be one of Literal values.
#             Defaults to None.
#         name (str | None, optional): If error raised, name will be printed. Defaults to None.

#     Raises:
#         ValidationError: Type does not fit.

#     Examples:
#         >>> from typing_extensions import Literal
#         ...
#         >>> validate(1, int)
#         >>> validate(None, list | None)
#         >>> validate("two", Literal["one", "two"])
#         >>> validate("three", Literal["one", "two"])
#         Traceback (most recent call last):
#         ValidationError: ...
#     """
#     check_type(value=value, expected_type=allowed_type, argname=name)

# TODO Wrap error with colors and remove stack only to configuration line...
# try:
#     check_type(value=value, expected_type=allowed_type, argname=name)
# except TypeError:

#     # ValidationError(mylogging.format_str("validate"))

#     raise


def small_validate(value, allowed_type: None | Any = None, name: str | None = None) -> None:
    """Type validation. It also works for Union and validate Literal values.

    Instead of typeguard validation, it define just subset of types, but is simplier
    and needs no extra import, therefore can be faster.

    Args:
        value (Any): Value that will be validated.
        allowed_type (Any, optional): For example int, str or list. It can be also Union or Literal.
            If Literal, validated value has to be one of Literal values. If None, it's skipped.
            Defaults to None.
        name (str | None, optional): If error raised, name will be printed. Defaults to None.

    Raises:
        TypeError: Type does not fit.

    Examples:
        >>> from typing_extensions import Literal
        ...
        >>> small_validate(1, int)
        >>> small_validate(None, Union[list, None])
        >>> small_validate("two", Literal["one", "two"])
        >>> small_validate("three", Literal["one", "two"])  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValidationError: ...
    """
    if allowed_type:
        # If Union
        if get_origin(allowed_type) == Union:

            if type(value) in get_args(allowed_type):
                return
            else:
                raise ValidationError(
                    mylogging.format_str(
                        f"Allowed type for variable '{name}' are {allowed_type}, but you try to set an {type(value)}"
                    )
                )

        # If Literal - parse options
        elif get_origin(allowed_type) == Literal:
            options = getattr(allowed_type, "__args__")
            if value in options:
                return
            else:
                raise ValidationError(
                    f"New value < {value} > for variable < {name} > is not in allowed options {options}."
                )

        else:
            if isinstance(value, allowed_type):  # type: ignore
                return
            else:
                raise ValidationError(
                    f"Allowed allowed_type for variable < {name} > is {allowed_type}, but you try to set an {type(value)}"
                )
