class Node:

    def __init__(self, key: any, data: any = None, parent = None, left = None, right = None):
        self.key = key
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self) -> str:
        output = f"[key: {self.key}, data: {self.data}, "
        output += f"parent: {f"[key: {self.parent.key}]" if self.parent is not None else None}, "
        output += f"left: {f"[key: {self.left.key}]" if self.left is not None else None}, "
        output += f"right: {f"[key: {self.right.key}]" if self.right is not None else None}]"
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

    def __init__(self, key: any, data: any = None, parent = None, left = None, right = None):
        super().__init__(key, data, parent, left, right)
        self.height = 0 if self.key is None else 1

    def __repr__(self) -> str:
        output = f"[key: {self.key}, data: {self.data}, "
        output += f"p: {f"[k: {self.parent.key}]" if self.parent is not None else "/"}, "
        output += f"l: {f"[k: {self.left.key}]" if self.left is not None else "/"}, "
        output += f"r: {f"[k: {self.right.key}]" if self.right is not None else "/"}, "
        output += f"h: {self.height}, balance: {self.balance()}]"
        return output

    
    def update_height(self):
        if self.key is None:
            self.height = 0
            return
        left = 0 if self.left is None else self.left.height
        right = 0 if self.right is None else self.right.height
        self.height = 1 + max(left, right)
    
    def balance(self) -> int:
        left = 0 if self.left is None else self.left.height
        right = 0 if self.right is None else self.right.height
        return left - right

class RBNode(Node):

    def __init__(self, key: any, data: any = None, parent = None, left = None, right = None):
        super().__init__(key, data, parent, left, right)
        self.black = True

    def __repr__(self) -> str:
        output = super().__repr__()[:-1]
        output += f", {'black' if self.black else 'red'}]"
        return output