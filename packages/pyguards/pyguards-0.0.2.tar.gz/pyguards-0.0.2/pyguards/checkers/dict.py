from .type import checkIsGoodType


def checkDictTypeContent(value: dict, typeExpected, **kwargs):
    checkIsGoodType(value, dict, **kwargs)
    for key, entity in value.items():
        checkIsGoodType(entity, typeExpected, **
                        {'attribute': '%s[\'%s\']' % (kwargs.get('attribute', 'value'), key)})
