from .type import checkIsGoodType


def checkDictTypeContent(value: dict, typeExpected: type, **kwargs):
    """
    Purpose of this checker is check if content of dict provided is defined and it's content of type provided.
    In wrong case, checker raise AttributeError.

    Args:
        value (dict): dict inspected by checker
        typeExpected (type): Type expected for object given

    Kwargs:
        attribute (str): Name of attribute used in exception message. Defaults to value

    Raises:
        AttributeError: Exception raised if object is undefined or misstyped

    Examples:

        For dict defined with correct typed entries :
            >>> checkDictTypeContent({'example':'example', 'os':'tux', 'reddit':'r/placeTux'}, str)

        For list defined with misstyped entries :
            >>> checkDictTypeContent({'example':123, 'os':'tux', 'reddit':'r/placeTux'}, str)
            Traceback (most recent call last):
                ...
            AttributeError: value['example'] must be a str (instead a int)

        For list defined with misstyped entries and custom attribute name  :
            >>> checkDictTypeContent({'example':123, 'os':'tux', 'reddit':'r/placeTux'}, str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example['example'] must be a str (instead a int)

        For list defined with undefined entries :
            >>> checkDictTypeContent({'example':None, 'os':'tux', 'reddit':'r/placeTux'}, str)
            Traceback (most recent call last):
                ...
            AttributeError: value['example'] must be defined

        For list defined with undefined entries and custom attribute name  :
            >>> checkDictTypeContent({'example':None, 'os':'tux', 'reddit':'r/placeTux'}, str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example['example'] must be defined

        For value misstyped :
            >>> checkDictTypeContent('str', str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be a dict (instead a str)

        For value misstyped with custom attribute name  :
            >>> checkDictTypeContent('str', str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be a dict (instead a str)

        For value undefined :
            >>> checkDictTypeContent(None, str)
            Traceback (most recent call last):
                ...
            AttributeError: value must be defined

        For value undefined with custom attribute name  :
            >>> checkDictTypeContent(None, str, **{'attribute': 'example'})
            Traceback (most recent call last):
                ...
            AttributeError: example must be defined
    """
    checkIsGoodType(value, dict, **kwargs)
    for key, entity in value.items():
        checkIsGoodType(entity, typeExpected, **
                        {'attribute': '%s[\'%s\']' % (kwargs.get('attribute', 'value'), key)})
