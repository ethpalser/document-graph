from tree import *

class TreeMap():

    def __init__(self) -> None:
        self.map = {}
        self.tree = RBTree()

    def find(self, key):
        return self.map[key]

    def insert(self, key, value):
        self.tree.insert(key, value)
        self.map[key] = value

    def delete(self, key):
        self.tree.delete(key)
        del self.map[key]