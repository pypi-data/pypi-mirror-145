from .checkers import checkListTypeContent, checkDictTypeContent, checkIsDefined


def raiseAssembledListErrors(errors: list):
    checkListTypeContent(errors, Exception, **{'attribute': 'errors'})
    if len(errors) > 0:
        allArgs = []
        for error in errors:
            allArgs.append(error.args)
        raise AttributeError(allArgs)


def raiseAssembledDictErrors(errors: dict):
    checkDictTypeContent(errors, Exception, **{'attribute': 'errors'})
    if len(errors.keys()) > 0:
        allArgs = {}
        for key, error in errors.items():
            allArgs[key] = error.args
        raise AttributeError(allArgs)


def raiseAssembledErrors(errors):
    checkIsDefined(errors, **{'attribute': 'errors'})
    if type(errors) is list:
        raiseAssembledListErrors(errors)
    elif type(errors) is dict:
        raiseAssembledDictErrors(errors)
    else:
        raise NotImplementedError(
            'For raiseAssembledErrors, %s isn\'t managed' % type(errors).__name__)
