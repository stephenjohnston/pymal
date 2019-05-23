class Symbol:
    def __init__(self, val):
        self.val = val

    def getVal(self):
        return self.val

    def str(self):
        return f'[Symbol {self.val}]'
