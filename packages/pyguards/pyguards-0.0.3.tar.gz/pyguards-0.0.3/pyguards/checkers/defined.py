def checkIsDefined(value: object, **kwargs):
    """
    Purpose of this checker is check if value provided is defined.
    In wrong case, checker raise AttributeError.

    Args:
        value (object): Object inspected by checker

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object is undefined

    Examples:

        For object defined :
            >>> example = '123'
            >>> checkIsDefined(example)

        For object undefined :
            >>> example = None
            >>> checkIsDefined(example)
            Traceback (most recent call last):
                ...
            AttributeError: value must be defined

        For object undefined with custom attribute name :
            >>> example = None
            >>> checkIsDefined(example, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be defined
    """
    if value is None:
        raise AttributeError("%s must be defined" %
                             kwargs.get('attribute', 'value'))
