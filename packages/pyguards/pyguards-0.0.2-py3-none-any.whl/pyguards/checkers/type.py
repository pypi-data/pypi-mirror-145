from .defined import checkIsDefined


def checkIsGoodType(value, typeExpected, **kwargs):
    checkIsDefined(value, **kwargs)
    checkTypeIfDefined(value, typeExpected, **kwargs)


def checkTypeIfDefined(value, typeExpected, **kwargs):
    if value is not None and not isinstance(value, typeExpected):
        raise AttributeError("%s must be a %s (instead a %s)" %
                             (kwargs.get('attribute', 'value'), typeExpected.__name__, type(value).__name__))
