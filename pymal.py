import readline
import reader
import tokenhelp
import symbols
import env
import core


def mal_read():
    s = input('user> ')
    return reader.read_str(s)


def eval_ast(ast, environ):
    if isinstance(ast, symbols.Symbol):
        fn = environ.get(ast.getVal())
        return fn
    elif isinstance(ast, list):
        newlist = list(map(lambda m: mal_eval(m, environ), ast))
        return newlist
    else:
        return ast


def update_env(e, l):
    it = iter(l)
    for x in it:
        e.set(x.getVal(), mal_eval(next(it), e))


def mal_eval(ast, environ):
    if not isinstance(ast, list):
        return eval_ast(ast, environ)
    elif len(ast) == 0:
        return ast
    else:
        if isinstance(ast[0], symbols.Symbol):
            if ast[0].getVal() == 'def!':
                environ.set(ast[1].getVal(), mal_eval(ast[2], environ))
                return environ.get(ast[1].getVal())
            elif ast[0].getVal() == 'let*':
                e = env.Env(environ)
                update_env(e, ast[1]);
                b = mal_eval(ast[2], e)
                return b
            elif ast[0].getVal() == 'if':
                b = mal_eval(ast[1], environ)
                if b != tokenhelp.SpecialToken.NIL and b is not False:
                    return mal_eval(ast[2], environ)
                else:
                    if len(ast) < 4:
                        return tokenhelp.SpecialToken.NIL
                    else:
                        return mal_eval(ast[3], environ)
            elif ast[0].getVal() == 'do':
                last = None
                for i in ast[1:]:
                    last = mal_eval(i, environ)
                return last
            elif ast[0].getVal() == 'fn*':
                return lambda *x: mal_eval(ast[2], env.Env(environ, ast[1].getVal(), x))
            elif ast[0].getVal() == 'defn':
                fn = lambda *x: mal_eval(ast[3], env.Env(environ, ast[2].getVal(), x))
                environ.set(ast[1].getVal(), fn)
                return environ.get(ast[1].getVal())

    eval_list = eval_ast(ast, environ)
    fn = eval_list[0]
    args = eval_list[1:]
    return fn(*args)


def mal_print(mal):
    print(reader.pr_str(mal))


def rep(environ):
    ast = mal_read()
    if ast != tokenhelp.SpecialToken.COMMENT and (not isinstance(ast, symbols.Symbol) or ast.getVal() != ''):
        e_ast = mal_eval(ast, environ)
        mal_print(e_ast)


def main():
    repl_env = env.Env(None)
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
            print(f"Error: {e.args[0]}")


if __name__ == '__main__':
    main()
