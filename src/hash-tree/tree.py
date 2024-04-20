from node import Node

class Tree:

    def __init__(self):
        self.nil = Node(None, None)
        self.root = self.nil

    def find(self, key) -> Node:
        curr = self.root
        while curr != self.nil and key != curr.key:
            if key < curr.key:
                curr = curr.left
            else: # > curr.key
                curr = curr.right
        return curr
    
    def insert(self, key, data):
        if key is None:
            raise Exception("key cannot be none")
        new_node = Node(key, data)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil

        parent = None
        curr = self.root
        while curr != self.nil:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                # duplicate key, ignore insert
                return
        

        if parent is None:
            self.root = new_node
        else:
            new_node.parent = parent
            if key < parent.key:
                parent.left = new_node
            else: # > parent.key
                parent.right = new_node

    def delete(self, key) -> bool:
        to_delete: Node = self.find(key)
        if to_delete == self.nil:
            return False
        
        to_replace: Node
        # This is a leaf node
        if to_delete.left == self.nil and to_delete.right == self.nil:
            to_replace = self.nil
        # Only a left child
        elif to_delete.left != self.nil and to_delete.right == self.nil:
            to_replace = to_delete.left
        # Only a right child
        elif to_delete.right != self.nil and to_delete.left == self.nil:
            to_replace = to_delete.right
        # Has both children
        else:
            # Fetch the next largest node to replace the one being deleted
            right_min: Node = to_delete.right
            while right_min.left != self.nil:
                right_min = right_min.left
            # Move the replacing node's child to its location
            if right_min.right != self.nil:
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
