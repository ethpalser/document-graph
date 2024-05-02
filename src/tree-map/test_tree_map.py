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

if __name__ == '__main__':
    unittest.main()