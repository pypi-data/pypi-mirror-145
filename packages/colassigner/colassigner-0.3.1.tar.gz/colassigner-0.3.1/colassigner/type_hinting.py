from typing import ForwardRef, Generic, TypeVar

T = TypeVar("T")

ERR_TXT = "return type hint not wrapped in Col[...]"


class Col(Generic[T]):
    pass


def get_hint_col_type(rethint):
    assert is_type_hint_origin(rethint, Col), ERR_TXT
    arg = rethint.__args__[0]
    if isinstance(arg, ForwardRef):
        return arg.__forward_arg__
    return arg


def is_type_hint_origin(hint, cls):
    try:
        return hint.__origin__ is cls
    except AttributeError:
        return False


def get_return_hint(fun):
    ret_annotation = getattr(fun, "__annotations__", {}).get("return")
    if ret_annotation is None:
        return None
    return get_hint_col_type(ret_annotation)
