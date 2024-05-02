from tree import *

class TreeMap():

    def __init__(self) -> None:
        self.map = {}
        self.tree = RBTree()

    def find(self, key):
        try:
            return self.map[key]
        except KeyError:
            return None

    def insert(self, key, value):
        self.tree.insert(key, value)
        self.map.update({key: value})

    def delete(self, key):
        if self.find(key) is None:
            return
        self.tree.delete(key)
        del self.map[key]
    
    def iter(self):
        return self.tree.iter()