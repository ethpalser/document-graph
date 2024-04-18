from node import Node

class AVLNode(Node):

    def __init__(self, data = None, left = None, right = None):
        super().__init__(data, left, right)
        self.balance = 0
