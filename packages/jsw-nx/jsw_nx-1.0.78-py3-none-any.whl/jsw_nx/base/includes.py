from .index import index
from .type import type


def includes(target, value):
    the_type = type(target)

    if the_type == 'str':
        return value in target
    elif the_type == 'list':
        return index(target, value) > 0
    elif the_type == 'dict':
        return value in target.values()
    else:
        return False
