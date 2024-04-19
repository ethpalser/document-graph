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

class AVLNode(Node):

    def __init__(self, data = None, left = None, right = None, parent = None):
        super().__init__(data, left, right, parent)
        self.balance = 0

    def __repr__(self) -> str:
        return super().__repr__()

class RBNode(Node):

    def __init__(self, data = None, left = None, right = None, parent = None):
        super().__init__(data, left, right, parent)
        self.black = True

    def __repr__(self) -> str:
        return super().__repr__()