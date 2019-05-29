from enum import Enum


class SpecialToken(Enum):
    NIL = 1
    COMMENT = 2


class Function:
    def __init__(self, ast_body, params, env, fn, is_macro = False):
        self.ast_body = ast_body
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro

    def get_params(self):
        return self.params

    def get_env(self):
        return self.env

    def get_ast_body(self):
        return self.ast_body

    def get_fn(self):
        return self.fn

    def get_is_macro(self):
        return self.is_macro
