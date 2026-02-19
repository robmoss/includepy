"""
Example functions for inclusion in a code block.
"""


def something(arg1, arg2):
    return f"{arg1} and {arg2}"


def hello(name: str) -> None:
    print(f"Hello {name}!")


def factorial(n: int) -> int:
    value = n  # (1)
    while n > 1:
        n -= 1
        value *= n
    return value


def duplicated() -> int:
    return 1


def duplicated() -> int:  # noqa: F811
    return 2


class MyClass:
    def do_thing(self, value: str) -> str:
        return f"MyClass: {value}"
