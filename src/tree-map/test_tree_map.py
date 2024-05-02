import unittest

from tree_map import TreeMap

class TestTreeMap(unittest.TestCase):

    def test_find_given_empty(self):
        map = TreeMap()
        actual = map.find(1)
        self.assertIsNone(actual)
    
    def test_find_given_missing(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(2, 'b')
        map.insert(3, 'c')
        map.insert(4, 'd')
        map.insert(5, 'e')

        actual = map.find(6)
        self.assertIsNone(actual)

    def test_find_given_exists(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(2, 'b')
        map.insert(3, 'c')
        map.insert(4, 'd')
        map.insert(5, 'e')

        actual = map.find(3)
        self.assertIsNotNone(actual)

    def test_insert_given_empty(self):
        map = TreeMap()
        map.insert(1, 'a')
        # This access is not recommended, but checking that it exists in tree
        self.assertIsNotNone(map.tree.root)
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[1])

    def test_insert_given_tree_of_one(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(2, 'b')
        # This access is not recommended, but checking that it exists in tree
        self.assertIsNotNone(map.tree.root.right)
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[2])

    def test_insert_given_tree_of_many(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(2, 'b')
        map.insert(3, 'c')
        # Not checking the tree, as its structure can change from rebalancing
        # This access is not recommended, but checking that it exists in dictionary
        self.assertIsNotNone(map.map[3])

    def test_delete_given_empty(self):
        map = TreeMap()
        map.delete(1)
        self.assertIsNone(map.find(1))

    def test_delete_given_tree_of_one(self):
        map = TreeMap()
        map.insert(1, 'a')
        self.assertIsNotNone(map.find(1))
        map.delete(1)
        self.assertIsNone(map.find(1))
    
    def test_delete_given_tree_of_many(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(2, 'b')
        map.insert(3, 'c')
        map.insert(4, 'd')
        map.insert(5, 'e')
        map.insert(6, 'f')

        self.assertIsNotNone(map.find(3))
        map.delete(3)
        self.assertIsNone(map.find(3))

    def test_iter_given_empty(self):
        map = TreeMap()
        iterator = map.iter()
        items = []
        count = 0
        for item in iterator:
            items.append(item.key)
            if count > 1:
                raise Exception("Iterator working longer than expected. It may not have been stopped correctly.")
            count += 1
        self.assertSequenceEqual(items, [])
    
    def test_iter_given_tree_of_one(self):
        map = TreeMap()
        map.insert(1, 'a')
        iterator = map.iter()
        items = []
        count = 0
        for item in iterator:
            items.append(item.data if item is not None else None)
            if count > 2:
                raise Exception("Iterator working longer than expected. It may not have been stopped correctly.")
            count += 1
        self.assertSequenceEqual(items, ['a'])
    
    def test_iter_given_tree_of_many(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(3, 'c')
        map.insert(5, 'e')
        map.insert(7, 'g')
        map.insert(9, 'i')
        map.insert(11, 'k')
        map.insert(13, 'm')
        map.insert(6, 'f')
        iterator = map.iter()
        items = []
        count = 0
        for item in iterator:
            items.append(item.data if item is not None else None)
            if count > 10:
                raise Exception("Iterator working longer than expected. It may not have been stopped correctly.")
            count += 1
        self.assertSequenceEqual(items, ['a', 'c', 'e', 'f', 'g', 'i', 'k', 'm'])

    # Verifying that the tree structure within the tree map also has its elements deleted
    def test_iter_given_tree_of_many_after_delete(self):
        map = TreeMap()
        map.insert(1, 'a')
        map.insert(3, 'c')
        map.insert(5, 'e')
        map.insert(7, 'g')
        map.insert(9, 'i')
        map.insert(11, 'k')
        map.insert(13, 'm')
        map.insert(6, 'f')

        map.delete(5)
        iterator = map.iter()
        items = []
        count = 0
        for item in iterator:
            items.append(item.data if item is not None else None)
            if count > 10:
                raise Exception("Iterator working longer than expected. It may not have been stopped correctly.")
            count += 1
        self.assertSequenceEqual(items, ['a', 'c', 'f', 'g', 'i', 'k', 'm'])

if __name__ == '__main__':
    unittest.main()