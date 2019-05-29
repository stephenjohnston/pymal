class Env:
    def __init__(self, outer, binds=None, exprs=None):
        self.data = {}
        self.outer = outer
        if binds is not None and exprs is not None:
            for b, e in zip(binds, exprs):
                self.set(b.getVal(), e)

    def set(self, key, mal):
        self.data[key] = mal

    def find(self, key):
        if key in self.data:
            return self.data
        elif self.outer is not None:
            return self.outer.find(key)
        else:
            return None

    def get(self, key):
        env = self.find(key)
        if env is not None:
            return env[key]
        else:
            raise Exception(f"undefined identifier: '{key}'")

    def contains(self, key):
        env = self.find(key)
        return env is not None
