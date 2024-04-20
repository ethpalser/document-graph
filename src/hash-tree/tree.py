from node import Node
from node import *

class Tree:

    def __init__(self, root: Node = None):
        self.root = root

    def find(self, key) -> Node:
        return self.__find(key, self.root)
        
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
        self.__insert(node, self.root)

    def __insert(self, node: Node, root: Node):
        if node < root:
            if root.left is None:
                node.parent = root
                root.left = node
            else:
                self.__insert(node, root.left)
        else:
            if root.right is None:
                node.parent = root
                root.right = node
            else:
                self.__insert(node, root.right)

    def delete(self, key) -> bool:
        to_delete: Node = self.find(key)
        if to_delete is None:
            return False
        
        to_replace: Node
        # This is a leaf node
        if to_delete.left is None and to_delete.right is None:
            to_replace = None
        # Only a left child
        elif to_delete.left is not None and to_delete.right is None:
            to_replace = to_delete.left
        # Only a right child
        elif to_delete.right is not None and to_delete.left is None:
            to_replace = to_delete.right
        # Has both children
        else:
            # Fetch the next largest node to replace the one being deleted
            right_min: Node = to_delete.right
            while right_min.left is not None:
                right_min = right_min.left
            # Move the replacing node's child to its location
            if right_min.right is not None:
                right_min.parent.left = right_min.right
            right_min.left = to_delete.left
            
            # Determine if this is a child of the node being deleted
            if to_delete.right != right_min:
                right_min.right = to_delete.right
            to_replace = right_min

        if to_delete.parent is None:
            self.root = to_replace
        else:
            # Determine which child of the parent this is
            match to_delete:
                case to_delete.parent.left:
                    to_delete.parent.left = to_replace
                case to_delete.parent.right:
                    to_delete.parent.right = to_replace
                case _:
                    raise Exception("Something went wrong: Node has a parent, but is not one of its children.")
        # Removing references for clean up
        to_delete.left = None
        to_delete.right = None
        del to_delete
        return True
