from node import *

class Tree:

    def __init__(self, root: Node):
        self.root = root

    def find(self, key) -> Node:
        return self.__find(self, key, self.root)
        
    def __find(self, key, root: Node) -> Node:
        if root is None or key is None:
            return None
        if key == root.key:
            return root
        
        left = self.__find(key, root.left)
        if left is not None:
            return left
        
        right = self.__find(key, root.right)
        if right is not None:
            return right
        return None
    
    def insert(self, node: Node):
        if self.root is None:
            self.root = node
            return
        self.__insert(self, node, self.root)

    def __insert(self, node: Node, root: Node):
        if node < root:
            if root.left is None:
                root.left = node
            else:
                self.__insert(node, root.left)
        else:
            if root.right is None:
                root.right = node
            else:
                self.__insert(node, root.right)