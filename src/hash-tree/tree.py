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
        return self._insert_node(new_node)

    def delete(self, key) -> bool:
        to_delete: Node = self.find(key)
        replacement: Node = self._delete_node(to_delete)
        # This is only when to_delete is None or nil (not found)
        if replacement is None:
            return False
        return True

    # General Node-manipulating methods

    def _insert_node(self, new_node: Node):
        parent = None
        curr = self.root
        while curr != self.nil:
            parent = curr
            if new_node.key < curr.key:
                curr = curr.left
            elif new_node.key > curr.key:
                curr = curr.right
            else:
                # duplicate key, ignore insert
                return
        
        if parent is None:
            self.root = new_node
        else:
            new_node.parent = parent
            if new_node.key < parent.key:
                parent.left = new_node
            else: # > parent.key
                parent.right = new_node
    
    def _delete_node(self, to_delete: Node) -> Node:
        if to_delete is None or to_delete == self.nil:
            return None
        
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

            if to_delete.right != right_min:
                # Move the replacing node's only potential child to take its place
                right_min.parent.left = right_min.right
                right_min.right = to_delete.right
            right_min.left = to_delete.left
            to_replace = right_min

        if to_delete.parent is None:
            self.root = to_replace
        else:
            # Determine which child of the parent this is
            if self._left_child(to_delete):
                to_delete.parent.left = to_replace
            else:
                to_delete.parent.right = to_replace
        # Update parent references
        to_replace.parent = to_delete.parent
        if to_delete.left is not None and to_delete.left != self.nil and to_delete.left != to_replace:
            to_delete.left.parent = to_replace
        if to_delete.right is not None and to_delete.right != self.nil and to_delete.right != to_replace:
            to_delete.right.parent = to_replace
        # Removing references for clean up
        to_delete.left = None
        to_delete.right = None
        del to_delete
        # Return the replacing node for processing
        return to_replace

    def _left_child(self, node: Node) -> bool:
        if node.parent is None:
            raise Exception(f"This node does not have a parent. {node}")
        match node:
            case node.parent.left:
                return True
            case node.parent.right:
                return False
            case _:
                raise Exception(f"Node is not a child of its parent. {node}")

    def _rotate_left(self, node: Node):
        if node is None or node == self.nil or node.right == self.nil:
            return
        temp = node.right.left
        node.right.left = node
        parent = node.parent
        node.right.parent = parent
        if parent is not None and parent != self.nil:
            if self._left_child(node):
                parent.left = node.right
            else:
                parent.right = node.right
        else:
            self.root = node.right

        node.parent = node.right
        node.right = temp

    def _rotate_right(self, node: Node):
        if node is None or node == self.nil or node.left == self.nil:
            return
        temp = node.left.right
        node.left.right = node
        parent = node.parent
        node.left.parent = parent
        if parent is not None:
            if self._left_child(node):
                parent.left = node.left
            else:
                parent.right = node.left
        else:
            self.root = node.left

        node.parent = node.left
        node.left = temp

class AVLTree(Tree):

    def __init__(self):
        self.nil = AVLNode(None, None)
        self.root = self.nil

    def _balance_tree(self, node: AVLNode):
        if node is None:
            return
        while node.parent is not None:
            # Ensure that this node has the correct height for balancing
            node.update_height()
            parent = node.parent # Maintain record, as it will change for node
            if self._left_child(node):
                # left imbalance
                if parent.balance() > 1:
                    # node with larger right
                    if node.balance() < 0:
                        self._rotate_left(node)
                        self._rotate_right(parent)
                    else:
                        self._rotate_right(parent)
                elif parent.balance() < 0:
                    # imbalance will be absorbed by node
                    break
            else:
                # right imbalance
                if parent.balance() < -1:
                    # node with larger left
                    if node.balance() > 0:
                        self._rotate_right(node)
                        self._rotate_left(parent)
                    elif node.balance() < 0:
                        self._rotate_left(parent)
                elif parent.balance() > 0:
                    # imbalance will be absorbed by node
                    break
            node = parent
    
    def insert(self, key, data):
        if key is None:
            raise Exception("key cannot be none")
        new_node = AVLNode(key, data)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil

        super()._insert_node(new_node)
        self._balance_tree(new_node)

    def delete(self, key) -> bool:
        to_delete: Node = self.find(key)
        replacement: Node = super()._delete_node(to_delete)
        if replacement is None:
            return False
        self._balance_tree(replacement)
        return True
    
class RBTree(Tree):
    
    def insert(self, key, data):
        return super().insert(key, data)
    
    def delete(self, key) -> bool:
        return super().delete(key)
