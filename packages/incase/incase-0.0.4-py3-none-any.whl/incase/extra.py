from cgitb import text
import enum
import functools
import typing as t
import warnings
import weakref
import textwrap

from incase.core import Case, Caseless


DO_NOT_TOUCH = [
    "__name__",
    "__doc__",
    "__package__",
    "__loader__",
    "__spec__",
    "__file__",
    "__cached__",
    "__builtins__",
]


def _incase_iterable(case: t.Iterable, value: t.Iterable) -> t.Iterable:
    return (Caseless(target)[case] for case, target in zip(case, value))


def _incase_single(case: str | Case, value: str | Case | dict | t.Iterable) -> str:
    if not value:
        return value
    if isinstance(value, (str, Case)):
        return Caseless(value)[case]
    elif isinstance(value, dict):
        return {k: _incase_single(case, v) for k, v in value.items()}
    else:
        try:
            if iter(value):
                generator = (_incase_single(case, v) for v in value)
                if isinstance(value, (list, tuple, set)):
                    return type(value)(generator)
                else:
                    return generator
        except TypeError:
            return value


@functools.singledispatch
def incase(case: t.Any, value: t.Any) -> t.Callable:
    if not value:
        return value
    # Enum is not a class and so single dispatch doesn't work on it...
    if isinstance(case, Case):
        return _incase_single(case.name, value)
    else:
        raise NotImplementedError(f"incase does not support type: {type(case)}")


@incase.register
def _(case: str, value: str | Case) -> dict:
    return _incase_single(case, value)


@incase.register
def _(case: list, incaseable: t.Iterable) -> t.List:
    return list(_incase_iterable(case, incaseable))


@incase.register
def _(case: dict, value: dict) -> dict:
    if isinstance(value, dict):
        return {k: Caseless(v)[case[k]] for k, v in value.items()}
    else:

        return incase(case[value], value) if value in case else value


def case_modifier(
    args_case: t.Sequence | str | Case | None = None,
    kwargs_case: dict | str | Case | None = None,
    keywords_case: str | Case | None = None,
    output_case: t.Sequence | str | Case | dict | None = None,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            args = incase(args_case, args) if args_case else args
            kwargs = incase(kwargs_case, kwargs) if kwargs_case else kwargs
            kwargs = (
                {incase(keywords_case, k): v for k, v in kwargs.items()}
                if keywords_case
                else kwargs
            )
            return incase(output_case, func(*args, **kwargs))

        return functools.wraps(func)(wrapper)

    return decorator


def planetary_defense_shield(case: str | Case, globals: dict):
    warnings.warn(
        textwrap.dedent(
            """
                                You have invoked the planetary defense shield.
                                This could have unknown consequences. 
                                At the least, it will increase the memory use of your code. 
                                It is not a good idea in production."""
        )
    )
    new_values = {}
    for k in globals.keys():
        if (
            k not in DO_NOT_TOUCH
            and k != (newname := incase(case, k))
            and newname not in globals
        ):
            print(f"cloaning {k} to {newname}")
            try:
                new_values[newname] = weakref.proxy(globals()[k])
            except TypeError:
                new_values[newname] = globals[k]

    globals.update(new_values)
