from .defined import checkIsDefined


def checkIsGoodType(value: object, typeExpected: type, **kwargs):
    """
    Purpose of this checker is check if value provided is defined and is instance of type provided.
    In wrong case, checker raise AttributeError.

    Args:
        value (object): Object inspected by checker
        typeExpected (type): Type expected for object given

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object is undefined or misstyped

    Examples:

        For object defined with correct type :
            >>> example = 'example'
            >>> checkIsGoodType(example, str)

        For object undefined :
            >>> example = None
            >>> checkIsGoodType(example, object)
            Traceback (most recent call last):
                ...
            AttributeError: value must be defined

        For object undefined with custom attribute name  :
            >>> example = None
            >>> checkIsGoodType(example, object, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be defined

        For object defined with wrong type :
            >>> example = object()
            >>> checkIsGoodType(example, str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be a str (instead a object)

        For object defined with wrong type and custom attribute name  :
            >>> example = 'example'
            >>> checkIsGoodType(example, int, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a int (instead a str)
    """
    checkIsDefined(value, **kwargs)
    checkTypeIfDefined(value, typeExpected, **kwargs)


def checkTypeIfDefined(value: object, typeExpected: type, **kwargs):
    """
    Purpose of this checker is check if value provided is instance of type provided if value is defined.
    In wrong case, checker raise AttributeError.

    Args:
        value (object): Object inspected by checker
        typeExpected (type): Type expected for object given

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object is defined and misstyped

    Examples:

        For object defined with correct type :
            >>> example = 'example'
            >>> checkTypeIfDefined(example, str)

        For object undefined :
            >>> example = None
            >>> checkTypeIfDefined(example, object)

        For object defined with wrong type :
            >>> example = object()
            >>> checkTypeIfDefined(example, str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be a str (instead a object)

        For object defined with wrong type and with custom error msg :
            >>> example = 'example'
            >>> checkTypeIfDefined(example, int, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a int (instead a str)
    """
    if value is not None and not isinstance(value, typeExpected):
        raise AttributeError("%s must be a %s (instead a %s)" %
                             (kwargs.get('attribute', 'value'), typeExpected.__name__, type(value).__name__))
