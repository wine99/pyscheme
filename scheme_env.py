import math
from scheme_types import Symbol, Pair
from scheme_types import PrimitiveProcedure


class Environment:
    def __init__(self, bindings: dict, base) -> None:
        self.bindings = bindings
        self.base = base


the_empty_environment = None


"""
@param params: list of Symbols
"""
def extend_environment(params: Pair, args: Pair, base: Environment):
    param_list = [param for param in params]
    arg_list = [arg for arg in args]
    if len(param_list) < len(arg_list):
        raise SyntaxError('Too many arguments')
    elif len(param_list) > len(arg_list):
        raise SyntaxError('Too few arguments')
    return Environment(dict(zip(param_list, arg_list)), base)


def lookup_variable_value(var: Symbol, env: Environment):
    frame = env
    while frame != the_empty_environment:
        if var in frame.bindings:
            return frame.bindings[var]
        frame = env.base
    raise RuntimeError(f'Unbound variable: {Symbol}')


def set_variable_value(var: Symbol, val, env: Environment):
    frame = env
    while frame != the_empty_environment:
        if var in frame.bindings:
            frame.bindings[var] = val
            return 'ok'
        frame = env.base
    raise RuntimeError(f'Unbound variable: {Symbol}')


def define_variable(var: Symbol, val, env: Environment):
    env.bindings[var] = val
    return 'ok'


the_global_environment = extend_environment(
    {
        Symbol('true'): True,
        Symbol('false'): False,
        Symbol('car'): PrimitiveProcedure(lambda pair: pair.car),
        Symbol('cdr'): PrimitiveProcedure(lambda pair: pair.cdr),
        Symbol('cons'): PrimitiveProcedure(lambda a, b: Pair(a, b)),
        Symbol('+'): PrimitiveProcedure(lambda *ops: sum(ops)),
        Symbol('-'): PrimitiveProcedure(lambda a, b: a - b),
        Symbol('*'): PrimitiveProcedure(lambda *ops: math.prod(ops)),
        Symbol('/'): PrimitiveProcedure(lambda a, b: a / b)
    },
    the_empty_environment
)
