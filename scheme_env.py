import math
from scheme_types import Symbol, Pair, the_empty_list
from scheme_types import PrimitiveProcedure
from primitive_procedures import scheme_not, scheme_and, scheme_or


class Environment:
    def __init__(self, bindings: dict, base) -> None:
        self.bindings = bindings
        self.base = base


the_empty_environment = None


def extend_environment(params: list, args: list, base: Environment):
    """
    @param params: list of Symbols
    """
    if len(params) < len(args):
        raise Exception("Too many arguments")
    elif len(params) > len(args):
        raise Exception("Too few arguments")
    return Environment(dict(zip(params, args)), base)


def lookup_variable_value(var: Symbol, env: Environment):
    frame = env
    while frame != the_empty_environment:
        if var in frame.bindings:
            return frame.bindings[var]
        frame = frame.base
    raise Exception(f"Unbound variable: {var}")


def set_variable_value(var: Symbol, val, env: Environment):
    frame = env
    while frame != the_empty_environment:
        if var in frame.bindings:
            frame.bindings[var] = val
            return 'ok'
        frame = env.base
    raise Exception(f"Unbound variable: {var}")


def define_variable(var: Symbol, val, env: Environment):
    env.bindings[var] = val
    return 'ok'


def setup_environment():
    global_environment = extend_environment([], [], the_empty_environment)
    global_bindings = {
        Symbol('true'): True,
        Symbol('false'): False,
        Symbol('nil'): the_empty_list,
        Symbol('car'): PrimitiveProcedure(lambda pair: pair.car),
        Symbol('cdr'): PrimitiveProcedure(lambda pair: pair.cdr),
        Symbol('cons'): PrimitiveProcedure(lambda a, b: Pair(a, b)),
        Symbol('+'): PrimitiveProcedure(lambda *ops: sum(ops)),
        Symbol('-'): PrimitiveProcedure(lambda a, b: a - b),
        Symbol('*'): PrimitiveProcedure(lambda *ops: math.prod(ops)),
        Symbol('/'): PrimitiveProcedure(lambda a, b: a / b),
        Symbol('<'): PrimitiveProcedure(lambda a, b: a < b),
        Symbol('>'): PrimitiveProcedure(lambda a, b: a > b),
        Symbol('<='): PrimitiveProcedure(lambda a, b: a <= b),
        Symbol('>='): PrimitiveProcedure(lambda a, b: a >= b),
        Symbol('='): PrimitiveProcedure(lambda a, b: a == b),
        Symbol('not'): PrimitiveProcedure(scheme_not),
        Symbol('and'): PrimitiveProcedure(scheme_and),
        Symbol('or'): PrimitiveProcedure(scheme_or),
        Symbol('exit'): PrimitiveProcedure(lambda: exit())
    }
    global_environment.bindings = global_bindings
    return global_environment
