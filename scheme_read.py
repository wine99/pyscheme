from scheme_types import Symbol, Pair, TheEmptyList, the_empty_list
from buffered_stream import BufferedStream


def scheme_read(f: BufferedStream):
    f.remove_whitespace()
    c = f.getc()
    if is_number(c, f.peek()):
        f.ungetc(c)
        return read_number(f)
    if c == '#':
        c = f.getc()
        if c == 't':
            return True
        if c == 'f':
            return False
        if c == '\\':
            return read_character(f)
        raise Exception(f"Boolean value must be #t or #f, not #{c}")
    if is_initial(c):
        f.ungetc(c)
        return read_symbol(f)
    if c == '\"':
        return read_string(f)
    if c == '(':
        return read_pair(f)
    raise Exception("Unknown syntax")


def read_character(f: BufferedStream) -> str:
    c = f.getc()
    next_c = f.peek()
    if c == 's' and next_c == 'p':
        read_expected_string(f, "pace", c)
        return ' '
    if c == 'n' and next_c == 'e':
        read_expected_string(f, "ewline", c)
        return '\n'
    if next_c != ' ' or next_c != '\n' or next_c != ';':
        raise Exception(f"Invalid character {c}{next_c}...")
    return c


def read_expected_string(f: BufferedStream,
                         expected_string: str,
                         initial_c: str) -> None:
    """
    Consume expected characters from the input buffer.
    @param initial_c This parameter is only for print error message.
    """
    c = f.getc()
    string_read = [c]
    for i in range(len(expected_string)):
        if c == expected_string[i]:
            c = f.getc()
            string_read.append(c)
        else:
            raise Exception(f"Invalid character {initial_c}{string_read}...")


def read_string(f: BufferedStream) -> str:
    buf = []
    c = f.getc()
    while c != '\"':
        buf.append(c)
        c = f.getc()
    return ''.join(buf)


def read_symbol(f: BufferedStream) -> Symbol:
    buf = []
    c = f.getc()
    while not is_delimiter(c):
        buf.append(c)
        c = f.getc()
    f.ungetc(c)
    return Symbol(''.join(buf))


def read_pair(f: BufferedStream) -> Pair or TheEmptyList:
    f.remove_whitespace()
    c = f.getc()
    if c == ')':
        return the_empty_list
    f.ungetc(c)
    car = scheme_read(f)
    f.remove_whitespace()
    cdr = read_pair(f)
    return Pair(car, cdr)


def read_number(f: BufferedStream) -> int or float:
    buf = []
    c = f.getc()
    while not is_delimiter(c):
        buf.append(c)
        c = f.getc()
    f.ungetc(c)
    buf = ''.join(buf)
    if '.' in buf:
        return float(buf)
    elif '/' in buf:
        raise Exception("Rational not implemented")
    else:
        return int(buf)


def is_delimiter(c: str) -> bool:
    return c in (' ', '(', ')', '\"', ';', '\n') or c is None


def is_initial(c: str) -> bool:
    return c.isalpha() or c in '+-*/<>=?!&'


def is_number(c: str, next_c: str) -> bool:
    return c.isdigit() or \
        (c == '.' and next_c.isdigit()) or \
        (c == '-' and (next_c == '.' or next_c.isdigit()))
