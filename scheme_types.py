class Symbol:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

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
        return '(' + ' '.join([str(e) for e in list(self)]) + ')'


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
