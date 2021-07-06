from scheme_types import is_true


def scheme_not(value):
    return not is_true(value)


def scheme_and(*values):
    for value in values:
        if not is_true(value):
            return False
    return values[-1]


def scheme_or(*values):
    for value in values:
        if is_true(value):
            return value
    return False
