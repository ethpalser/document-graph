from unittest import TestCase

from node import Node
from tree import Tree

class TestTree(TestCase):

    def test_find_given_empty_tree_then_none(self):
        tree = Tree()
        result = tree.find(1)
        self.assertIsNone(result)

    def test_find_given_tree_and_root_match_then_root(self):
        key = 1
        root = Node(key)
        tree = Tree(root)
        result = tree.find(1)
        self.assertIsNotNone(result)
        self.assertEqual(root, result)

    def test_find_given_tree_and_no_match_then_none(self):
        key = 1
        root = Node(key)
        tree = Tree(root)
        result = tree.find(0)
        self.assertIsNone(result)

    def test_insert_given_empty_tree_then_root_tree(self):
        root = Node(20)
        tree = Tree()
        tree.insert(root)
        self.assertEqual(root, tree.root)

    def test_insert_given_tree_and_smaller_key_then_inserted_left(self):
        tree = Tree(Node(10))
        node = Node(5)
        tree.insert(node)
        self.assertEqual(node, tree.root.left)

    def test_insert_given_tree_and_larger_key_then_inserted_right(self):
        tree = Tree(Node(10))
        node = Node(15)
        tree.insert(node)
        self.assertEqual(node, tree.root.right)

    # This tree does not ignore duplicate keys, and does not overwrite
    def test_insert_given_tree_and_equal_key_then_inserted_right(self):
        key = "blue"
        tree = Tree(Node(key))
        node = Node(key)
        tree.insert(node)
        self.assertEqual(node, tree.root.right)
        self.assertNotEqual(node, tree.root)

    def test_delete_given_empty_tree_then_false(self):
        tree = Tree()
        result = tree.delete(1)
        self.assertFalse(result)

    def test_delete_given_tree_with_no_children_and_found_then_true_and_empty(self):
        tree = Tree(Node(1.1))
        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertIsNone(tree.root)

    def test_delete_given_tree_with_children_and_found_then_true_and_right(self):
        tree = Tree(Node(1.1))
        left = Node(1.0)
        tree.insert(left)
        right = Node(1.2)
        tree.insert(right)
        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertEqual(right, tree.root)

    def test_delete_given_tree_with_no_right_child_and_found_then_true_and_left(self):
        tree = Tree(Node(1.1))
        left = Node(1.0)
        tree.insert(left)
        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertEqual(left, tree.root)

    def test_delete_given_tree_and_found_child_then_true(self):
        # Given
        tree = Tree(Node(5))
        left = Node(2)
        left_l = Node(1)
        left_r = Node(3)
        right = Node(8)
        right_l = Node(6)
        right_r = Node(9)
        # Note: It is not recommended to manually set the left and right outside the tree
        tree.insert(left)
        tree.insert(left_l)
        tree.insert(right_r)
        tree.insert(right)
        tree.insert(right_l)
        tree.insert(right_r)
        # When
        result = tree.delete(8)
        self.assertTrue(result)
        self.assertEqual(tree.root.right, right_r)