class Vector:
    def __init__(self, list):
        self.list = list

    def getVal(self):
        return self.list

    def __iter__(self):
        return self.list.__iter__()

    def __getitem__(self, item):
        return self.list[item]