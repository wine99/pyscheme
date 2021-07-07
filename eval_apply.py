'''
exp -> int
     | float
     | str
     | bool
     | the_empty_list
     | Symbol
     | Pair (list of <exp>)
'''

from scheme_types import Symbol, Pair, the_empty_list
from scheme_types import is_null, is_true
from scheme_types import PrimitiveProcedure, CompoundProcedure
from scheme_env import lookup_variable_value
from scheme_env import set_variable_value, define_variable
from scheme_env import extend_environment

from buffered_stream import BufferedStream
from scheme_read import scheme_read


def meval(exp, env):
    # primitives
    if is_self_evaluating(exp):
        return exp
    if is_variable(exp):
        return lookup_variable_value(exp, env)
    # special forms
    if is_quoted(exp):
        return text_of_quotation(exp)
    if is_assignment(exp):
        return eval_assignment(exp, env)
    if is_definition(exp):
        return eval_definition(exp, env)
    if is_if(exp):
        return eval_if(exp, env)
    if is_lambda(exp):
        return make_procedure(lambda_parameters(exp), lambda_body(exp), env)
    if is_begin(exp):
        return [meval(e, env) for e in begin_actions(exp)][-1]
    # if is_cond(exp):
    #     return meval(cond_to_if(exp), env)
    # combinations
    if is_load(exp):
        return eval_load(exp, env)
    if is_application(exp):
        return mapply(meval(operator(exp), env),
                      [meval(e, env) for e in operands(exp)])
    raise Exception("Unknown expression type")


def mapply(procedure, arguments):
    if is_primitive_procedure(procedure):
        return primitive_proc_underlying_proc(procedure)(*arguments)
    elif is_compound_procedure(procedure):
        new_env = extend_environment(procedure_parameters(procedure),
                                     arguments,
                                     procedure_environment(procedure))
        return [meval(e, new_env) for e in procedure_body(procedure)][-1]


def eval_if(exp, env):
    if is_true(meval(if_predicate(exp), env)):
        return meval(if_consequent(exp), env)
    else:
        return meval(if_alternative(exp), env)


def eval_assignment(exp, env):
    set_variable_value(assignment_variable(exp),
                       meval(assignment_value(exp), env),
                       env)
    return 'ok'


def eval_definition(exp, env):
    define_variable(definition_variable(exp),
                    meval(definition_value(exp), env),
                    env)
    return 'ok'


def is_self_evaluating(exp):
    return isinstance(exp, int) or \
           isinstance(exp, float) or \
           isinstance(exp, str) or \
           isinstance(exp, bool) or \
           is_null(exp)


def is_variable(exp):
    return isinstance(exp, Symbol)


def is_quoted(exp):
    return exp.car == Symbol('quote')

def text_of_quotation(exp):
    return exp.cdr.car


def is_assignment(exp):
    return exp.car == Symbol('set!')

def assignment_variable(exp):
    return exp.cdr.car

def assignment_value(exp):
    return exp.cdr.cdr.car


'''
(define <var> <val>)
OR
(define (<var> <param_1> ... <param_n>)
  <body>)
->
(define <var>
  (lambda (<param_1> ... <param_n>)
    <body>))
'''

def is_definition(exp):
    return exp.car == Symbol('define')

def definition_variable(exp):
    if isinstance(exp.cdr.car, Symbol):
        return exp.cdr.car
    else:
        return exp.cdr.car.car

def definition_value(exp):
    if isinstance(exp.cdr.car, Symbol):
        return exp.cdr.cdr.car
    else:
        return make_lambda(exp.cdr.car.cdr, exp.cdr.cdr)


def is_lambda(exp):
    return exp.car == Symbol('lambda')

def lambda_parameters(exp):
    return exp.cdr.car

def lambda_body(exp):
    return exp.cdr.cdr

def make_lambda(params, body):
    return Pair(Symbol('lambda'), Pair(params, body))


def is_if(exp):
    return exp.car == Symbol('if')

def if_predicate(exp):
    return exp.cdr.car

def if_consequent(exp):
    return exp.cdr.cdr.car

def if_alternative(exp):
    if is_null(exp.cdr.cdr.cdr):
        return exp.cdr.cdr.cdr.car
    else:
        return Symbol('false')

def make_if(predicate, consequent, alternative):
    return Pair(Symbol('if'),
                Pair(predicate,
                     Pair(consequent,
                          Pair(alternative, the_empty_list))))


def is_begin(exp):
    return exp.car == Symbol('begin')

def begin_actions(exp):
    return exp.cdr

def is_last_exp(seq):
    return is_null(seq.cdr)

def first_exp(seq):
    return seq.car

def rest_exps(seq):
    return seq.cdr

def sequence_to_exp(seq):
    if is_null(seq):
        return seq
    elif is_last_exp(seq):
        return first_exp(seq)
    else:
        return Pair(Symbol('begin'), seq)


def is_application(exp):
    return isinstance(exp, Pair)

def operator(exp):
    return exp.car

def operands(exp):
    return exp.cdr


# TODO cond


def is_load(exp):
    return exp.car == Symbol('load')

def eval_load(exp, env):
    result = 'ok'
    with open(load_filename(exp), 'r') as file:
        f = BufferedStream(file)
        while f.peek():
            result = meval(scheme_read(f), env)
            f.remove_whitespace()
    return result

def load_filename(exp):
    return exp.cdr.car


def is_primitive_procedure(proc):
    return isinstance(proc, PrimitiveProcedure)

def primitive_proc_underlying_proc(proc: PrimitiveProcedure):
    return proc.underlying_primitive_proc


def make_procedure(params, body, env):
    return CompoundProcedure(params, body, env)

def is_compound_procedure(proc):
    return isinstance(proc, CompoundProcedure)

def procedure_parameters(proc: CompoundProcedure):
    return proc.parameters

def procedure_body(proc: CompoundProcedure):
    return proc.body

def procedure_environment(proc: CompoundProcedure):
    return proc.environment
