from .defined import checkIsDefined
from .type import checkIsGoodType


def checkInBounds(value: object, lowerBound: object, higherBound: object, **kwargs):
    """
    Purpose of this checker is check if value provided is in bounds provided.
    In wrong case, checker raise AttributeError.

    Args:
        value (object): Object inspected by checker
        lowerBound (object): Lower value accepted for object given
        higherBound (object): Higher value accepted for object given

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object isn't in bounds

    Examples:

        For object in two bounds :
            >>> checkInBounds(1.5, 1.0, 2.0)

        For object below higherBound :
            >>> checkInBounds(2.0, None, 90.0)

        For object not below lowerBound :
            >>> checkInBounds(0, -12, None)

        For object not in two bounds :
            >>> checkInBounds(0, 2, 3)
            Traceback (most recent call last):
                ...
            AttributeError: value must be in following bounds (2-3)

        For object not in two bounds with custom attribute name :
            >>> checkInBounds(0, 2, 3, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be in following bounds (2-3)

        For object not below higherBound :
            >>> checkInBounds(18, None, 3)
            Traceback (most recent call last):
                ...
            AttributeError: value must be in following bounds (<=3)

        For object not below higherBound with custom attribute name :
            >>> checkInBounds(18, None, 3, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be in following bounds (<=3)

        For object below lowerBound :
            >>> checkInBounds(0, 2, None)
            Traceback (most recent call last):
                ...
            AttributeError: value must be in following bounds (>=2)

        For object below lowerBound with custom attribute name :
            >>> checkInBounds(0, 2, None, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be in following bounds (>=2)

        For object with type missmatch with bounds :
            >>> checkInBounds('0', 2, 3)
            Traceback (most recent call last):
                ...
            AttributeError: value must be a int (instead a str)

        For object with type missmatch with bounds and custom attribute name :
            >>> checkInBounds('0', 2, 3, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a int (instead a str)

        For bounds undefined :
            >>> checkInBounds(2, None, None)
            Traceback (most recent call last):
                ...
            AttributeError: bounds must be defined
    """
    checkIsDefined(lowerBound if lowerBound is not None else higherBound,
                   **{'attribute': 'bounds'})
    typeOfBound = type(
        lowerBound) if lowerBound is not None else type(higherBound)
    checkIsGoodType(value, typeOfBound, **kwargs)
    if (lowerBound is not None and value < lowerBound) or (higherBound is not None and value > higherBound):
        raise AttributeError(
            "%s must be in following bounds (%s)" % (
                kwargs.get('attribute', 'value'),
                (
                    "%s-%s" % (lowerBound, higherBound) if lowerBound is not None and higherBound is not None
                    else "%s%s" % ('>=', lowerBound) if lowerBound is not None else "%s%s" % ('<=', higherBound)
                )
            )
        )
