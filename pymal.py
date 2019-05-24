import readline
import reader
import tokenhelp
import symbols
import env
import core
import vector


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


def update_env(e, lst):
    if isinstance(lst, vector.Vector):
        l2 = lst.getVal()
    else:
        l2 = lst
    it = iter(l2)
    for x in it:
        e.set(x.getVal(), mal_eval(next(it), e))


def mal_eval(ast, environ):
    while True:
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
                    environ = e
                    ast = ast[2]
                    continue
                elif ast[0].getVal() == 'if':
                    b = mal_eval(ast[1], environ)
                    if b != tokenhelp.SpecialToken.NIL and b is not False:
                        ast = ast[2]
                    else:
                        if len(ast) < 4:
                            ast = tokenhelp.SpecialToken.NIL
                        else:
                            ast = ast[3]
                    continue
                elif ast[0].getVal() == 'do':
                    for i in ast[1:len(ast)-1]:
                        mal_eval(i, environ)
                    ast = ast[len(ast)-1]
                    continue
                elif ast[0].getVal() == 'fn*':
                    return tokenhelp.Function(ast[2], ast[1].getVal(), environ,
                                              lambda *x: mal_eval(ast[2], env.Env(environ, ast[1].getVal(), x)))
                elif ast[0].getVal() == 'defn':
                    f = tokenhelp.Function(ast[3], ast[2].getVal(), environ,
                                           lambda *x: mal_eval(ast[3], env.Env(environ, ast[2].getVal(), x)))
                    environ.set(ast[1].getVal(), f)
                    return f

            eval_list = eval_ast(ast, environ)
            if isinstance(eval_list[0], tokenhelp.Function):
                ast = eval_list[0].get_ast_body()
                environ = env.Env(eval_list[0].get_env(), eval_list[0].get_params(), eval_list[1:])
                continue
            else:
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
