from typing import List

__all__ = ["InvalidFilters", "InputError", "EmptyInput"]


class InvalidFilters(Exception):
    """Invalid filter input"""

    def __init__(self, fields: List):
        msg = '. '.join([f'{f}' for f in fields])
        message = f'Invalid filters: {msg}'
        super().__init__(message)


class InputError(Exception):
    """Invalid input."""


class EmptyInput(Exception):
    """Empty input."""
