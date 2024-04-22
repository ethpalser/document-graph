from node import Node, AVLNode, RBNode

class Tree:

    def __init__(self):
        self.nil = Node(None, None)
        self.root = self.nil

    def __repr__(self) -> str:
        return self.__print_tree(0, self.root)

    def __print_tree(self, height, node):
        if node is None or node == self.nil:
            return ""
        branch = self.__print_tree(height + 1, node.right)
        branch += "\n"
        for i in range(0, height):
            branch += "      "
        branch += f"k:{node.key}"
        if node.left != self.nil or node.right != self.nil:
            branch += " <"
        branch += self.__print_tree(height + 1, node.left)
        return branch

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

class AVLTree(Tree):

    def __init__(self):
        self.nil = AVLNode(None, None)
        self.root = self.nil

    def find(self, key) -> AVLNode:
        curr = self.root
        while curr != self.nil and key != curr.key:
            if key < curr.key:
                curr = curr.left
            else: # > curr.key
                curr = curr.right
        return curr
        

    def _left_child(self, node: Node) -> bool:
        if node.parent is None:
            raise Exception(f"This node does not have a parent. {node}")
        match node:
            case node.parent.left:
                return True
            case node.parent.right:
                return False
            case _:
                raise Exception(f"Node is not a child of its parent.")

    def _rotate_left(self, node: AVLNode):
        if node is None or node == self.nil or node.right == self.nil:
            return
        temp = node.right.left
        node.right.left = node
        node.right.parent = node.parent
        if node.parent is not None and node.parent != self.nil:
            if self._left_child(node):
                node.parent.left = node.right
            else:
                node.parent.right = node.right
        else:
            self.root = node.right

        node.parent = node.right
        node.right = temp
        node.update_height()
        node.parent.update_height()

    def _rotate_right(self, node: AVLNode):
        if node is None or node == self.nil or node.left == self.nil:
            return
        temp = node.left.right
        node.left.right = node
        node.left.parent = node.parent
        if node.parent is not None:
            if self._left_child(node):
                node.parent.left = node.left
            else:
                node.parent.right = node.left
        else:
            self.root = node.left

        node.parent = node.left
        node.left = temp
        node.update_height()
        node.parent.update_height()

    def _balance_tree(self, node: AVLNode):
        grandparent = None
        parent = node.parent
        while parent is not None:
            grandparent = parent.parent
            if self._left_child(node):
                # parent is left heavy
                if parent.balance() > 0:
                    # child is right heavy, creating a gt-shape imbalance
                    if node.balance() < 0:
                        self._rotate_left(node)
                        self._rotate_right(parent) # Node's new parent after rotation
                    elif node.balance() > 0:
                        self._rotate_right(parent)
                else:
                    if parent.balance() < 0:
                        # height change is absorbed
                        break
            else:
                # parent is right heavy
                if parent.balance() < 0:
                    # child is left heavy, creating a lt-shape imbalance
                    if node.balance() > 0:
                        self._rotate_right(node)
                        self._rotate_left(parent)
                    elif node.balance() < 0:
                        self._rotate_left(parent)
                else:
                    if parent.balance() > 0:
                        # height change is absorbed
                        break
            node = parent
            parent = grandparent
    
    def insert(self, key, data):
        if key is None:
            raise Exception("key cannot be none")
        new_node = AVLNode(key, data)
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
            to_resize = new_node
            while to_resize != None:
                to_resize.update_height()
                to_resize = to_resize.parent
        self._balance_tree(new_node)

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
        self._balance_tree(to_delete.parent)
        del to_delete
        return True
    
class RBTree(Tree):
    
    def insert(self, key, data):
        return super().insert(key, data)
    
    def delete(self, key) -> bool:
        return super().delete(key)
