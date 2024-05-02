import unittest

from tree_map import TreeMap

class TestTreeMap(unittest.TestCase):

    def test_find_given_empty(self):
        map = TreeMap()
        actual = map.find(1)
        self.assertIsNone(actual)
    
    def test_find_given_missing(self):
        map = TreeMap()
        map.insert(1, None)
        map.insert(2, None)
        map.insert(3, None)
        map.insert(4, None)
        map.insert(5, None)

        actual = map.find(6)
        self.assertIsNone(actual)

    def test_find_given_exists(self):
        map = TreeMap()
        map.insert(1, None)
        map.insert(2, None)
        map.insert(3, None)
        map.insert(4, None)
        map.insert(5, None)

        actual = map.find(3)
        self.assertIsNone(actual)

    def test_insert_given_empty(self):
        map = TreeMap()
        map.insert(1, None)
        # This access is not recommended, but checking that it exists in tree
        self.assertIsNotNone(map.tree.root)
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[1])

    def test_insert_given_tree_of_one(self):
        map = TreeMap()
        map.insert(1, None)
        map.insert(2, None)
        # This access is not recommended, but checking that it exists in tree
        self.assertIsNotNone(map.tree.root.right)
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[2])

    def test_insert_given_tree_of_many(self):
        map = TreeMap()
        map.insert(1, None)
        map.insert(2, None)
        map.insert(3, None)
        # Not checking the tree, as its structure can change from rebalancing
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[3])

    def test_delete_given_empty(self):
        map = TreeMap()
        map.delete(1)
        self.assertIsNone(map.find(1))

    def test_delete_given_tree_of_one(self):
        map = TreeMap()
        map.insert(1, None)
        self.assertIsNotNone(map.find(1))
        map.delete(1)
        self.assertIsNone(map.find(1))
    
    def test_delete_given_tree_of_many(self):
        map = TreeMap()
        map.insert(1, None)
        map.insert(2, None)
        map.insert(3, None)
        map.insert(4, None)
        map.insert(5, None)
        map.insert(6, None)

        self.assertIsNotNone(map.find(3))
        map.delete(3)
        self.assertIsNone(map.find(3))

if __name__ == '__main__':
    unittest.main()