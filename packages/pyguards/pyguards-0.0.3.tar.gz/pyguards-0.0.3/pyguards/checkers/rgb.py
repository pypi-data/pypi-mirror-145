from .bounds import checkInBounds
from .type import checkIsGoodType


def checkIsRGB(value: int, **kwargs):
    """
    Purpose of this checker is check if value provided is valid.
    In wrong case, checker raise AttributeError.

    Args:
        value (int): Object inspected by checker

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object isn't in bounds

    Examples:

        For correct RGB :
            >>> checkIsRGB(125)

        For value undefined :
            >>> checkIsRGB(None)
            Traceback (most recent call last):
                ...
            AttributeError: value must be defined

        For value undefined with custom attribute name :
            >>> checkIsRGB(None, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be defined

        For value misstyped :
            >>> checkIsRGB('12')
            Traceback (most recent call last):
                ...
            AttributeError: value must be a int (instead a str)

        For value misstyped with custom attribute name :
            >>> checkIsRGB('example', **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a int (instead a str)

        For value out of bounds :
            >>> checkIsRGB(256)
            Traceback (most recent call last):
                ...
            AttributeError: value must be in following bounds (0-255)

        For value out of bounds with custom attribute name :
            >>> checkIsRGB(256, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be in following bounds (0-255)
    """
    checkIsGoodType(value, int, **kwargs)
    checkInBounds(value, 0, 255, **kwargs)
