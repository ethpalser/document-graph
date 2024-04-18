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

    def delete(self, key):
        if self.root is None:
            return
        
        if key == self.root.key:
            if self.root.right is not None:
                self.root = self.root.right
            else:
                self.root.left = self.root.left
            return
        
        to_delete: Node = self.find(key)
        if to_delete is None or not isinstance(to_delete.parent, Node):
            return
        
        replacement = to_delete.right if to_delete.right is not None else to_delete.left
        if to_delete.parent.right is not None and to_delete.key == to_delete.parent.right.key:
            to_delete.parent.right = replacement
        elif to_delete.parent.left is not None and to_delete.key == to_delete.parent.left.key:
            to_delete.parent.left = replacement
        else:
            raise Exception("Something went wrong: Node has a parent, but is not one of its children.")