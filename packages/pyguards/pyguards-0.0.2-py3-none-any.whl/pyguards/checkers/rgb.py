from .bounds import checkInBounds


def checkIsRGB(value, **kwargs):
    checkInBounds(value, 0, 255, **kwargs)
