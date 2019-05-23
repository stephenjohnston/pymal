import reader

def prn(a):
    print(reader.pr_str(a))
    return None

ns = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: int(a / b),
    'prn': prn,
    'str': lambda *x: ''.join(x),
    'list': lambda *x: list(x),
    'list?': lambda x: isinstance(x, list),
    'empty?': lambda x: len(x) == 0,
    'count': lambda x: len(x),
    '=': lambda a, b: a == b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    'quit': lambda: exit(0)
}
