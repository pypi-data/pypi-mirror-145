from typing import get_type_hints


def get_return_type(fn):
    return get_type_hints(fn).get("return")
