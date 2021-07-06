# from eval_apply import meval
from scheme_types import is_true
# from scheme_env import the_global_environment
# from scheme_read import scheme_read
# from buffered_stream import BufferedStream

'''
Other primitive procedures are in scheme_env.py
'''

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


# TODO load
# def scheme_load(filename):
#     with open(filename, 'r') as file:
#         f = BufferedStream(file)
#         while f.peek():
#             meval(scheme_read(f), the_global_environment)
#             f.remove_whitespace()
