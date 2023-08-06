from .defined import checkIsDefined
from .type import checkIsGoodType


def checkInBounds(value, lowerBound, higherBound, **kwargs):
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
