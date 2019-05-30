import readline
import reader
import core
from tokenhelp import Function, SpecialToken
from symbols import Symbol
from env import Env
from vector import Vector


def is_pair(lst):
    if isinstance(lst, list):
        return len(lst) > 0
    elif isinstance(lst, Vector):
        return len(lst.getVal())
    return False


def quasiquote(ast):
    if not is_pair(ast):
        return [Symbol("quote"), ast]
    elif isinstance(ast[0], Symbol) and ast[0].getVal() == "unquote":
        return ast[1]
    if is_pair(ast[0]) and isinstance(ast[0][0], Symbol) and ast[0][0].getVal() == "splice-unquote":
        return [Symbol("concat"), ast[0][1], quasiquote(ast[1:])]
    else:
        return [Symbol("cons"), quasiquote(ast[0]), quasiquote(ast[1:])]


def mal_read():
    s = input('user> ')
    return reader.read_str(s)


def eval_ast(ast, environ):
    if isinstance(ast, Symbol):
        fn = environ.get(ast.getVal())
        return fn
    elif isinstance(ast, list):
        newlist = list(map(lambda m: mal_eval(m, environ), ast))
        return newlist
    else:
        return ast


def update_env(e, lst):
    if isinstance(lst, Vector):
        l2 = lst.getVal()
    else:
        l2 = lst
    it = iter(l2)
    for x in it:
        e.set(x.getVal(), mal_eval(next(it), e))


def is_macro_call(ast, env):
    if isinstance(ast, list) and len(ast) > 0 and isinstance(ast[0], Symbol):
        if env.contains(ast[0].getVal()):
            fn = env.get(ast[0].getVal())
            ret_val = isinstance(fn, Function)
            if ret_val and fn.get_is_macro():
                return True
            else:
                return False
    else:
        return False


def macroexpand(ast, env):
    while is_macro_call(ast, env):
        fn = env.get(ast[0].getVal())
        real_fn = fn.get_fn()
        ast = real_fn(ast[1:])
    return ast


def mal_eval(ast, environ):
    while True:
        ast = macroexpand(ast, environ)
        if not isinstance(ast, list):
            return eval_ast(ast, environ)
        elif len(ast) == 0:
            return ast
        else:
            if isinstance(ast[0], Symbol):
                if ast[0].getVal() == 'def!':
                    environ.set(ast[1].getVal(), mal_eval(ast[2], environ))
                    return environ.get(ast[1].getVal())
                elif ast[0].getVal() == 'quote':
                    return ast[1];
                elif ast[0].getVal() == 'quasiquote':
                    ast = quasiquote(ast[1])
                    continue
                elif ast[0].getVal() == 'macroexpand':
                    return macroexpand(ast[1], environ)
                elif ast[0].getVal() == 'let*':
                    e = Env(environ)
                    update_env(e, ast[1]);
                    environ = e
                    ast = ast[2]
                    continue
                elif ast[0].getVal() == 'if':
                    b = mal_eval(ast[1], environ)
                    if b != SpecialToken.NIL and b is not False:
                        ast = ast[2]
                    else:
                        if len(ast) < 4:
                            ast = SpecialToken.NIL
                        else:
                            ast = ast[3]
                    continue
                elif ast[0].getVal() == 'do':
                    for i in ast[1:len(ast)-1]:
                        mal_eval(i, environ)
                    ast = ast[len(ast)-1]
                    continue
                elif ast[0].getVal() == 'fn*':
                    return Function(ast[2], ast[1].getVal(), environ,
                                              lambda *x: mal_eval(ast[2], Env(environ, ast[1].getVal(), x)))
                elif ast[0].getVal() == 'defn':
                    f = Function(ast[3], ast[2].getVal(), environ,
                                           lambda *x: mal_eval(ast[3], Env(environ, ast[2].getVal(), x)))
                    environ.set(ast[1].getVal(), f)
                    return f
                elif ast[0].getVal() == 'defmacro!':
                    f = Function(ast[3], ast[2].getVal(), environ,
                                           lambda *x: mal_eval(ast[3], Env(environ, ast[2].getVal(), x[0])), True)
                    environ.set(ast[1].getVal(), f)
                    return f

            eval_list = eval_ast(ast, environ)
            if isinstance(eval_list[0], Function):
                ast = eval_list[0].get_ast_body()
                environ = Env(eval_list[0].get_env(), eval_list[0].get_params(), eval_list[1:])
                continue
            else:
                fn = eval_list[0]
                args = eval_list[1:]
                return fn(*args)


def mal_print(mal):
    print(reader.pr_str(mal))


def rep(environ):
    ast = mal_read()
    if ast != SpecialToken.COMMENT and (not isinstance(ast, Symbol) or ast.getVal() != ''):
        e_ast = mal_eval(ast, environ)
        mal_print(e_ast)


def main():
    repl_env = Env(None)
    for k, v in core.ns.items():
        repl_env.set(k, v)

    repl_env.set('eval', lambda ast: mal_eval(ast, repl_env))

    readline.set_history_length(1000)

    for s in core.builtins:
        mal_eval(reader.read_str(s), repl_env)

    while True:
        try:
            rep(repl_env)
        except (EOFError, KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
