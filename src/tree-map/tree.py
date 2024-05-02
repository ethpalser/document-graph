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
        branch += f"k:{node.key}, black:{node.black}"
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

    def iter(self):
        return TreeIterator(self)

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

    def __init__(self):
        self.nil = RBNode(None)
        self.root = self.nil
    
    def _balance_tree(self, node: RBNode):
        if node is None:
            return
        
        while node.parent is not None:
            parent = node.parent
            if parent.parent is None:
                # Recolour to avoid red-violation
                if not parent.black:
                    parent.black = True
                break

            child_is_left = self._left_child(node)
            parent_is_left = self._left_child(parent)

            grandparent = parent.parent
            uncle = grandparent.right if parent_is_left else grandparent.left

            if not parent.black and not uncle.black:
                # Rebalancing is not needed, can recolour to avoid red-violation
                parent.black = True
                uncle.black = True
                grandparent.black = False
            elif not parent.black and uncle.black:
                if parent_is_left:
                    if not child_is_left:
                        self._rotate_left(parent)
                        # Set the current node to the demoted parent
                        node = parent
                        continue
                    else:
                        self._rotate_right(grandparent)
                        # Recolour to avoid red-violation with node and parent
                        parent.black = True
                        # Recolour to avoid black-violation
                        grandparent.black = False
                else:
                    if child_is_left:
                        self._rotate_right(parent)
                        # Set the current node to the demoted parent
                        node = parent
                        continue
                    else:
                        self._rotate_left(grandparent)
                        # Recolour to avoid red-violation with node and parent
                        parent.black = True
                        # Recolour to avoid black-violation
                        grandparent.black = False
            node = grandparent
        # Update the root to reflect rearranged structure
        if node.parent is None:
            self.root = node
            self.root.black = True

    def insert(self, key, data):
        if key is None:
            raise Exception("key cannot be none")
        new_node = RBNode(key, data)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.black = False

        super()._insert_node(new_node)
        self._balance_tree(new_node)
    
    def _balance_delete(self, replacement, deleted):
        # The replacement is the next successor (black) or an only child (red)
        if replacement != self.nil and not replacement.black:
            # This node has replaced its parent, recolour to remove red-violation
            replacement.black = True
            return
        
        # The replacement is for a leaf node (black or red)
        if replacement == self.nil:
            # Deleted red-leaf nodes will not break any properties
            if not deleted.black:
                return

        # A black-leaf node was deleted, a rebalance is required
        node = deleted
        node_is_left = True if deleted.parent is not None and deleted.parent.left == self.nil else False
        while node.parent is not None:
            parent = node.parent
            if parent is None:
                # The root, nothing is required
                return
        
            sibling = parent.right if node_is_left else parent.left
            close_nephew = parent.right.left if node_is_left else parent.left.right
            distant_nephew = parent.right.right if node_is_left else parent.left.left
            # sibling is red, close, distant and parent are black 
            if not sibling.black:
                # Move sibling to the location of the parent
                if node_is_left:
                    self._rotate_left(parent)
                else:
                    self._rotate_right(parent)
                sibling.black = True
                parent.black = False
                continue
            # close nephew is red, sibling and distant are black, parent is either
            if not close_nephew.black:
                if node_is_left:
                    self._rotate_right(sibling)
                else:
                    self._rotate_left(sibling)
                close_nephew.black = True
                sibling.black = False  
                continue
            # distant nephew is red, sibling and close are black, parent is either
            if not distant_nephew.black:
                if node_is_left:
                    self._rotate_left(parent)
                else:
                    self._rotate_right(parent)
                sibling.black = parent.black
                parent.black = True
                distant_nephew.black = True
                return
            
            if not parent.black and sibling.black and close_nephew.black and distant_nephew.black:
                parent.black = True
                sibling.black = False
                return
            else:
                sibling.black = False
                node = parent
                if node.parent is not None:
                    node_is_left = self._left_child(node)

    def delete(self, key) -> bool:
        to_delete = self.find(key)
        replacement = super()._delete_node(to_delete)
        if replacement is None:
            return False
        self._balance_delete(replacement, to_delete)
        return True

class TreeIterator():

    def __init__(self, tree: Tree):
        self.tree = tree
        self.prev = None
        self.prev_key = None
    
    def __iter__(self):
        return self

    def __next__(self) -> Node:
        next = self.tree.root if self.prev is None else self.prev
        # Start iterating through the binary tree without recursion
        # Note: Currently not safe from modification
        while True:
            # The root is nil, or a leaf node was unexpectedly used
            if next == self.tree.nil:
                raise StopIteration
            # Follow the left subtree for the next smallest
            while next.left != self.tree.nil:
                if self.prev_key is not None and next.left.key <= self.prev_key:
                    break
                next = next.left
            # Update variables and return the next node
            if next is not None and next != self.prev:
                self.prev_key = next.key
                self.prev = next
                return next
            # Go to the right subtree
            if next.right != self.tree.nil and next.right.key > self.prev_key:
                next = next.right
            # Go to the next smallest parent
            else:
                while next.parent is not None:
                    next = next.parent
                    if next.key > self.prev_key:
                        break
            # Iteration ends when the root is reached with no more larger keys (right tree) to visit
            if next == self.tree.root and next.key <= self.prev_key:
                raise StopIteration
            # Continue next cycle, looking for the next smallest key