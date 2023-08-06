class Attribute:
    def __init__(self, key, value, dom):
        self.key = key
        self.value = value
        self.dom = dom

    def toDict(self):
        return {self.key: self.value}