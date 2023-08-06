from .type import checkIsGoodType


def checkListTypeContent(value: list, typeExpected, **kwargs):
    checkIsGoodType(value, list, **kwargs)
    for index, entity in enumerate(value):
        checkIsGoodType(entity, typeExpected, **
                        {'attribute': '%s[%s]' % (kwargs.get('attribute', 'value'), index)})
