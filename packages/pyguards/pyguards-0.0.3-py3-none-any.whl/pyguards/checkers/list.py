from .type import checkIsGoodType


def checkListTypeContent(value: list, typeExpected: type, **kwargs):
    """
    Purpose of this checker is check if content of list provided is defined and it's content of type provided.
    In wrong case, checker raise AttributeError.

    Args:
        value (list): list inspected by checker
        typeExpected (type): Type expected for object given

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object is undefined or misstyped

    Examples:

        For list defined with correct typed entries :
            >>> checkListTypeContent(['example', 'tux', 'r/placeTux'], str)

        For list defined with misstyped entries :
            >>> checkListTypeContent(['example', 123, 'r/placeTux'], str)
            Traceback (most recent call last):
                ...
            AttributeError: value[1] must be a str (instead a int)

        For list defined with misstyped entries and custom attribute name  :
            >>> checkListTypeContent(['example', 123, 'r/placeTux'], str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example[1] must be a str (instead a int)

        For list defined with undefined entries :
            >>> checkListTypeContent(['example', None, 'r/placeTux'], str)
            Traceback (most recent call last):
                ...
            AttributeError: value[1] must be defined

        For list defined with undefined entries and custom attribute name  :
            >>> checkListTypeContent(['example', None, 'r/placeTux'], str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example[1] must be defined

        For value misstyped :
            >>> checkListTypeContent('str', str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be a list (instead a str)

        For value misstyped with custom attribute name  :
            >>> checkListTypeContent('str', str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a list (instead a str)

        For value undefined :
            >>> checkListTypeContent(None, str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be defined

        For value undefined with custom attribute name  :
            >>> checkListTypeContent(None, str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be defined
    """
    checkIsGoodType(value, list, **kwargs)
    for index, entity in enumerate(value):
        checkIsGoodType(entity, typeExpected, **
                        {'attribute': '%s[%s]' % (kwargs.get('attribute', 'value'), index)})
