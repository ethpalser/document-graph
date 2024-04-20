class Node:

    def __init__(self, key: any, data: any = None, left = None, right = None, parent = None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self) -> str:
        output = f"[key: {self.key}, data: {self.data}, "
        output += f"left: {f"[key: {self.left.key}]" if self.left is not None else None}, "
        output += f"right: {f"[key: {self.right.key}]" if self.right is not None else None}, "
        output += f"parent: {f"[key: {self.parent.key}]" if self.parent is not None else None}]"
        return output

    def __lt__(self, other: any) -> bool:
        if not isinstance(other, Node):
            return False
        # These keys should use types that can be compared using <
        return self.key < other.key
    
    def __eq__(self, other: any) -> bool:
        if not isinstance(other, Node):
            return False
        return self.key == other.key

class AVLNode(Node):

    def __init__(self, data = None, left = None, right = None, parent = None):
        super().__init__(data, left, right, parent)
        self.height = 0

    def __repr__(self) -> str:
        output = super().__repr__()[:-1]
        output += f", height: {self.height}]"
        return output
    
    def set_height(self):
        left = 0 if self.left is None else self.left.height
        right = 0 if self.right is None else self.right.height
        return 1 + max(left, right)
    
    def set_left(self, left):
        self.left = left
        self.set_height()

    def set_right(self, right):
        self.right = right
        self.set_height()

    def balance(self) -> int:
        left = 0 if self.left is None else self.left.height
        right = 0 if self.right is None else self.right.height
        return left - right

class RBNode(Node):

    def __init__(self, data = None, left = None, right = None, parent = None):
        super().__init__(data, left, right, parent)
        self.black = True

    def __repr__(self) -> str:
        return super().__repr__()