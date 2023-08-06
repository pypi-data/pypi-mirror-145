from .checkers import checkListTypeContent, checkDictTypeContent, checkIsDefined


def raiseAssembledListErrors(errors: list):
    """
    Purpose of utils is assemble errors from list

    Args:
        errors (list): list of errors to assemble before raise if isn't empty

    Raises:
        AttributeError: AssembledError if list isn't empty

    Examples:

        For some errors :
            >>> raiseAssembledListErrors([AttributeError('Example'), AttributeError('2nd Example')])
            Traceback (most recent call last):
                ...
            AttributeError: [('Example',), ('2nd Example',)]

        For no errors provided :
            >>> raiseAssembledListErrors([])

        For errors with content misstyped :
            >>> raiseAssembledListErrors([AttributeError('Example'), 'Example'])
            Traceback (most recent call last):
                ...
            AttributeError: errors[1] must be a Exception (instead a str)

        For errors with content undefined :
            >>> raiseAssembledListErrors([AttributeError('Example'), None])
            Traceback (most recent call last):
                ...
            AttributeError: errors[1] must be defined

        For errors misstyped :
            >>> raiseAssembledListErrors('example')
            Traceback (most recent call last):
                ...
            AttributeError: errors must be a list (instead a str)

        For errors undefined :
            >>> raiseAssembledListErrors(None)
            Traceback (most recent call last):
                ...
            AttributeError: errors must be defined
    """
    checkListTypeContent(errors, Exception, **{'attribute': 'errors'})
    if len(errors) > 0:
        allArgs = []
        for error in errors:
            allArgs.append(error.args)
        raise AttributeError(allArgs)


def raiseAssembledDictErrors(errors: dict):
    """
    Purpose of utils is assemble errors from dict

    Args:
        errors (dict): dict of errors to assemble before raise if isn't empty

    Raises:
        AttributeError: AssembledError if list isn't empty

    Examples:

        For some errors :
            >>> raiseAssembledDictErrors({'example': AttributeError('Example'), '2nd' : AttributeError('2nd Example')})
            Traceback (most recent call last):
                ...
            AttributeError: {'example': ('Example',), '2nd': ('2nd Example',)}

        For no errors provided :
            >>> raiseAssembledDictErrors({})

        For errors with content misstyped :
            >>> raiseAssembledDictErrors({'example': AttributeError('Example'), '2nd' : 'Example'})
            Traceback (most recent call last):
                ...
            AttributeError: errors['2nd'] must be a Exception (instead a str)

        For errors with content undefined :
            >>> raiseAssembledDictErrors({'example': AttributeError('Example'), '2nd' : None})
            Traceback (most recent call last):
                ...
            AttributeError: errors['2nd'] must be defined

        For errors misstyped :
            >>> raiseAssembledDictErrors('example')
            Traceback (most recent call last):
                ...
            AttributeError: errors must be a dict (instead a str)

        For errors undefined :
            >>> raiseAssembledDictErrors(None)
            Traceback (most recent call last):
                ...
            AttributeError: errors must be defined
    """
    checkDictTypeContent(errors, Exception, **{'attribute': 'errors'})
    if len(errors.keys()) > 0:
        allArgs = {}
        for key, error in errors.items():
            allArgs[key] = error.args
        raise AttributeError(allArgs)


def raiseAssembledErrors(errors: object):
    """
    Purpose of utils is assemble errors from object supported

    Args:
        errors (object): object contains errors to assemble before raise if isn't empty

    Raises:
        AttributeError: AssembledError if list isn't empty

    Examples:

        For some errors :
            >>> raiseAssembledErrors({'example': AttributeError('Example'), '2nd' : AttributeError('2nd Example')})
            Traceback (most recent call last):
                ...
            AttributeError: {'example': ('Example',), '2nd': ('2nd Example',)}
            >>> raiseAssembledErrors([AttributeError('Example'), AttributeError('2nd Example')])
            Traceback (most recent call last):
                ...
            AttributeError: [('Example',), ('2nd Example',)]

        For no errors provided :
            >>> raiseAssembledErrors({})
            >>> raiseAssembledErrors([])

        For errors with content misstyped :
            >>> raiseAssembledErrors({'example': AttributeError('Example'), '2nd' : 'Example'})
            Traceback (most recent call last):
                ...
            AttributeError: errors['2nd'] must be a Exception (instead a str)
            >>> raiseAssembledErrors([AttributeError('Example'), 'Example'])
            Traceback (most recent call last):
                ...
            AttributeError: errors[1] must be a Exception (instead a str)

        For errors with content undefined :
            >>> raiseAssembledErrors({'example': AttributeError('Example'), '2nd' : None})
            Traceback (most recent call last):
                ...
            AttributeError: errors['2nd'] must be defined
            >>> raiseAssembledErrors([AttributeError('Example'), None])
            Traceback (most recent call last):
                ...
            AttributeError: errors[1] must be defined

        For errors misstyped :
            >>> raiseAssembledErrors('example')
            Traceback (most recent call last):
                ...
            NotImplementedError: For raiseAssembledErrors, str isn't managed

        For errors undefined :
            >>> raiseAssembledErrors(None)
            Traceback (most recent call last):
                ...
            AttributeError: errors must be defined
    """
    checkIsDefined(errors, **{'attribute': 'errors'})
    if type(errors) is list:
        raiseAssembledListErrors(errors)
    elif type(errors) is dict:
        raiseAssembledDictErrors(errors)
    else:
        raise NotImplementedError(
            'For raiseAssembledErrors, %s isn\'t managed' % type(errors).__name__)
