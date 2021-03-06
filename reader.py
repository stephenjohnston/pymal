import re
from symbols import Symbol
from tokenhelp import Function, SpecialToken
from vector import Vector


class Reader:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def next(self):
        if self.index < len(self.tokens):
            self.index += 1
            return self.tokens[self.index - 1]
        else:
            return None

    def peek(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None


def tokenize(s):
    pattern = r'[\s,]*(~@|[\[\]{}()\'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}(\'"`,;)]*)'
    return re.findall(pattern, s)


def read_str(s):
    tokens = tokenize(s)
    r = Reader(tokens)
    return read_form(r)


def read_form(r):
    tok = r.peek()
    if tok == '(':
        return read_list(r)
    elif tok == '[':
        return read_vector(r)
    elif tok.startswith('"'):
        return read_string(r)
    elif tok == "'":
        r.next()
        return [Symbol('quote'), read_form(r)]
    elif tok == '`':
        r.next()
        return [Symbol('quasiquote'), read_form(r)]
    elif tok == '~':
        r.next()
        return [Symbol('unquote'), read_form(r)]
    elif tok == '~@':
        r.next()
        return [Symbol('splice-unquote'), read_form(r)]
    else:
        return read_atom(r)


def read_string(r):
    tok = r.next()
    return tok[1:len(tok)-1]


def read_vector(r):
    r.next()  # consume the paren
    rslt = []
    tok = read_form(r)
    while isinstance(tok, Symbol) is False or (isinstance(tok, Symbol) is True and tok.getVal() != ']'):
        if tok != SpecialToken.COMMENT:
            rslt.append(tok)
        tok = read_form(r)
    return Vector(rslt)


def read_list(r):
    r.next()  # consume the paren
    rslt = []
    tok = read_form(r)
    while isinstance(tok, Symbol) is False or (isinstance(tok, Symbol) is True and tok.getVal() != ')'):
        if tok != SpecialToken.COMMENT:
            rslt.append(tok)
        tok = read_form(r)
    return rslt


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read_atom(r):
    tok = r.next()
    if tok.isnumeric() or tok.replace('.', '').isnumeric():
        return num(tok)
    elif isinstance(tok, str):
        if tok == 'true':
            return True
        elif tok == 'false':
            return False
        elif tok == 'nil':
            return SpecialToken.NIL
        elif tok.startswith(';'):
            return SpecialToken.COMMENT
        else:
            return Symbol(tok)


def pr_str(mal):
    if mal is None:
        return "nil(None)"
    elif isinstance(mal, Symbol):
        return mal.getVal()
    elif isinstance(mal, Vector):
        s = ' '.join(map(pr_str, mal.getVal()))
        return '[' + s + ']'
    elif isinstance(mal, bool):
        return "true" if mal else "false"
    elif mal == SpecialToken.NIL:
        return "nil(NIL)"
    elif isinstance(mal, str):
        return '"' + mal + '"'
    elif isinstance(mal, list):
        s = ' '.join(map(pr_str, mal))
        return '(' + s + ')'
    elif callable(mal):
        return "#<function>"
    else:
        return str(mal)


def main():
    m = read_str('(map inc [1 2 3 4])')
    print(pr_str(m))


if __name__ == '__main__':
    main()