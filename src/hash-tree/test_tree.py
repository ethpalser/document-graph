from unittest import TestCase

from tree import Tree

class TestTree(TestCase):

    def test_find_given_empty_tree_then_none(self):
        tree = Tree()
        actual = tree.find(1)
        self.assertEqual(tree.nil, actual)

    def test_find_given_tree_and_root_match_then_root(self):
        tree = Tree()
        tree.insert(1, None)

        actual = tree.find(1)
        self.assertNotEqual(tree.nil, actual)

    def test_find_given_tree_and_no_match_then_none(self):
        tree = Tree()
        tree.insert(1, None)

        actual = tree.find(0)
        self.assertEqual(tree.nil, actual)

    def test_insert_given_empty_tree_then_root_tree(self):
        tree = Tree()
        tree.insert(20, None)

        self.assertNotEqual(tree.nil, tree.root)

    def test_insert_given_tree_and_smaller_key_then_inserted_left(self):
        tree = Tree()
        tree.insert(20, None)
        tree.insert(5, None)

        actual = tree.find(5)
        self.assertEqual(tree.root.left, actual)

    def test_insert_given_tree_and_larger_key_then_inserted_right(self):
        tree = Tree()
        tree.insert(10, None)
        tree.insert(15, None)

        actual = tree.find(15)
        self.assertEqual(tree.root.right, actual)

    def test_insert_given_tree_and_equal_key_then_not_inserted(self):
        key = "blue"
        tree = Tree()
        tree.insert(key, None)
        tree.insert(key, None)

        original = tree.find(key)
        self.assertEqual(tree.nil, original.left)
        self.assertEqual(tree.nil, original.right)

    def test_delete_given_empty_tree_then_false(self):
        tree = Tree()

        result = tree.delete(1)
        self.assertFalse(result)

    def test_delete_given_tree_with_no_children_and_found_then_true_and_empty(self):
        tree = Tree()
        tree.insert(1.1, None)

        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertEqual(tree.nil, tree.root)

    def test_delete_given_tree_with_children_and_found_then_true_and_right(self):
        tree = Tree()
        tree.insert(1.1, None)
        tree.insert(1.0, None) # Left
        tree.insert(1.2, None) # Right

        result = tree.delete(1.1)
        self.assertTrue(result)
        actual = tree.find(1.2)
        self.assertEqual(tree.root, actual)

    def test_delete_given_tree_with_no_right_child_and_found_then_true_and_left(self):
        tree = Tree()
        tree.insert(1.1, None)
        tree.insert(1.0, None)

        result = tree.delete(1.1)
        self.assertTrue(result)
        actual = tree.find(1.0)
        self.assertEqual(tree.root, actual)

    def test_delete_given_tree_and_found_child_then_true(self):
        # Given
        tree = Tree()
        tree.insert(5, None) # root
        tree.insert(2, None) # left
        tree.insert(1, None) # left.left
        tree.insert(3, None) # left.right
        tree.insert(8, None) # right
        tree.insert(6, None) # right.left
        tree.insert(9, None) # right.right

        # When
        result = tree.delete(8)
        self.assertTrue(result)
        actual = tree.find(9)
        self.assertEqual(tree.root.right, actual)