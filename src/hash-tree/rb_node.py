from node import Node

class RBNode(Node):

    def __init__(self, data = None, left = None, right = None):
        super().__init__(data, left, right)
        self.black = True
