class Node:

    def __init__(self, key: any, data: any = None, left = None, right = None):
        self.key = key
        self.data: data
        self.left: left
        self.right: right

    def __lt__(self, other: any) -> bool:
        if not isinstance(other, Node):
            return False
        # These keys should use types that can be compared using <
        return self.key < other.key

class AVLNode(Node):

    def __init__(self, data = None, left = None, right = None):
        super().__init__(data, left, right)
        self.balance = 0

class RBNode(Node):

    def __init__(self, data = None, left = None, right = None):
        super().__init__(data, left, right)
        self.black = True