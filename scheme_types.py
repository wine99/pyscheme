class Symbol:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Symbol) and self.name == o.name

    def __hash__(self) -> int:
        return self.name.__hash__()


class TheEmptyList:
    def __repr__(self) -> str:
        return '()'


the_empty_list = TheEmptyList()


def is_null(exp) -> bool:
    return isinstance(exp, TheEmptyList)


class Pair:
    def __init__(self, car, cdr) -> None:
        self.car = car
        self.cdr = cdr

    def __iter__(self):
        pair = self
        while not isinstance(pair, TheEmptyList):
            yield pair.car
            pair = pair.cdr

    def __repr__(self) -> str:
        return '(' + ' '.join([str(e) for e in self]) + ')'


class PrimitiveProcedure():
    def __init__(self, fn) -> None:
        self.underlying_primitive_proc = fn

    def __repr__(self) -> str:
        return "Primitive procedure"


class CompoundProcedure():
    def __init__(self, params, body, env) -> None:
        self.parameters = params
        self.body = body
        self.environment = env

    def __repr__(self) -> str:
        return "Compound procedure"


"""
Only False is false
"""
def is_true(val) -> bool:
    if isinstance(val, bool):
        return val
    if val == 0:
        return True
    if val == "":
        return True
    if is_null(val):
        return True
    return bool(val)


def pair_to_list(p: Pair) -> list:
    if is_null(p):
        return []
    return list(p)


def list_to_pair(lst: list) -> Pair:
    if not len(lst):
        return the_empty_list
    return Pair(lst[0], list_to_pair(lst[1:]))
