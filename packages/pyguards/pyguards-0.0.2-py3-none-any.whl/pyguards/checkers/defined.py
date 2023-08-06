def checkIsDefined(value, **kwargs):
    if value is None:
        raise AttributeError("%s must be defined" %
                             kwargs.get('attribute', 'value'))
