import unittest

from tree import *

class TestTree(unittest.TestCase):

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
        self.assertEqual(tree.find(1.1), tree.nil)
        self.assertEqual(tree.nil, tree.root)

    def test_delete_given_tree_with_children_and_found_then_true_and_right(self):
        tree = Tree()
        tree.insert(1.1, None)
        tree.insert(1.0, None) # Left
        tree.insert(1.2, None) # Right

        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertEqual(tree.find(1.1), tree.nil)
        self.assertEqual(tree.find(1.2), tree.root)

    def test_delete_given_tree_with_no_right_child_and_found_then_true_and_left(self):
        tree = Tree()
        tree.insert(1.1, None)
        tree.insert(1.0, None)

        result = tree.delete(1.1)
        self.assertTrue(result)
        self.assertEqual(tree.find(1.1), tree.nil)
        self.assertEqual(tree.find(1.0), tree.root)

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
        self.assertEqual(tree.find(9), tree.root.right)
        self.assertEqual(tree.find(6), tree.root.right.left)

class TestAVLTree(unittest.TestCase):

    def test_left_child_root(self):
        tree = AVLTree()
        tree.insert(1, None)
        self.assertRaises(Exception, lambda: tree._left_child(tree.root))

    def test_rotate_left_root_of_empty_tree(self):
        tree = AVLTree()
        tree._rotate_left(tree.root)
        self.assertEqual(tree.nil, tree.root)

    def test_rotate_left_root_of_root_tree(self):
        tree = AVLTree()
        tree.insert(1, None)
        tree._rotate_left(tree.root)
        self.assertEqual(tree.find(1), tree.root)

    def test_rotate_left_root_of_full_tree(self):
        tree = AVLTree()
        tree.insert(6, None) # root
        tree.insert(4, None) # left
        tree.insert(8, None) # right
        tree.insert(2, None) # left.left
        tree.insert(9, None) # right.right
        tree.insert(5, None) # left.right
        tree.insert(7, None) # right.left
        # No rebalancing should have occurred
        self.assertEqual(tree.find(6), tree.root)
        tree._rotate_left(tree.root)
        # The right is promoted up while the original is demoted to left
        self.assertEqual(tree.find(8), tree.root)
        self.assertEqual(tree.find(9), tree.root.right) # Unaffected by rotation
        self.assertEqual(tree.find(6), tree.root.left)
        self.assertEqual(tree.find(7), tree.root.left.right) # Affected by rotation

    def test_rotate_right_root_of_empty_tree(self):
        tree = AVLTree()
        tree._rotate_right(tree.root)
        self.assertEqual(tree.root, tree.nil)

    def test_rotate_right_root_of_root_tree(self):
        tree = AVLTree()
        tree.insert(1, None)
        tree._rotate_right(tree.root)
        self.assertEqual(tree.find(1), tree.root)

    def test_rotate_right_root_of_full_tree(self):
        tree = AVLTree()
        tree.insert(6, None) # root
        tree.insert(4, None) # left
        tree.insert(8, None) # right
        tree.insert(2, None) # left.left
        tree.insert(9, None) # right.right
        tree.insert(5, None) # left.right
        tree.insert(7, None) # right.left
        # No rebalancing should have occurred
        self.assertEqual(tree.find(6), tree.root)
        tree._rotate_right(tree.root)
        # The right is promoted up while the original is demoted to left
        self.assertEqual(tree.find(4), tree.root)
        self.assertEqual(tree.find(2), tree.root.left) # Unaffected by rotation
        self.assertEqual(tree.find(6), tree.root.right)
        self.assertEqual(tree.find(5), tree.root.right.left) # Affected by rotation
    
    def test_insert_with_left_rotation(self):
        tree = AVLTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None) # This will automatically rebalance once balance_tree is integrated
        latest = tree.find(3)
        tree._balance_tree(latest) # This does nothing if already balanced
        self.assertEqual(tree.find(2), tree.root)
        self.assertEqual(tree.find(1), tree.root.left)
        self.assertEqual(tree.find(3), tree.root.right)

    def test_insert_with_right_rotation(self):
        tree = AVLTree()
        tree.insert(3, None)
        tree.insert(2, None)
        tree.insert(1, None) # This will automatically rebalance once balance_tree is integrated
        latest = tree.find(1)
        tree._balance_tree(latest) # This does nothing if already balanced
        self.assertEqual(tree.find(2), tree.root)
        self.assertEqual(tree.find(1), tree.root.left)
        self.assertEqual(tree.find(3), tree.root.right)
    
    def test_insert_with_left_right_rotation(self):
        tree = AVLTree()
        tree.insert(9, None)
        tree.insert(5, None)
        tree.insert(7, None) # This will automatically rebalance once balance_tree is integrated
        latest = tree.find(7)
        tree._balance_tree(latest) # This does nothing if already balanced
        self.assertEqual(tree.find(7), tree.root)
        self.assertEqual(tree.find(5), tree.root.left)
        self.assertEqual(tree.find(9), tree.root.right)
        
    def test_insert_with_right_left_rotation(self):
        tree = AVLTree()
        tree.insert(5, None)
        tree.insert(9, None)
        tree.insert(7, None) # This will automatically rebalance once balance_tree is integrated
        latest = tree.find(7)
        tree._balance_tree(latest) # This does nothing if already balanced
        self.assertEqual(tree.find(7), tree.root)
        self.assertEqual(tree.find(5), tree.root.left)
        self.assertEqual(tree.find(9), tree.root.right)
    
    def test_insert_with_many_imbalances(self):
        tree = AVLTree()
        tree.insert(1, None) # root
        tree.insert(2, None) # balanced
        tree.insert(3, None) # rotate left 1 (root 2)
        tree.insert(4, None) # balanced
        tree.insert(5, None) # rotate left 3
        tree.insert(6, None) # rotate left 2 (root 4)
        tree.insert(7, None) # rotate left 5
        tree.insert(8, None) # balanced
        tree.insert(9, None) # rotate left 7
        tree.insert(10, None) # rotate left 6
        self.assertEqual(tree.find(4), tree.root)

    def test_delete_with_no_rotation(self):
        tree = AVLTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        self.assertEqual(tree.find(2), tree.root)
        result = tree.delete(2)
        self.assertTrue(result)
        self.assertEqual(tree.find(2), tree.nil)
        self.assertEqual(tree.find(3), tree.root)
        self.assertEqual(tree.root.right, tree.nil)

    def test_delete_with_no_rotation_using_next_largest(self):
        tree = AVLTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(4, None)
        tree.insert(3, None)
        self.assertEqual(tree.find(2), tree.root)
        result = tree.delete(2)
        self.assertTrue(result)
        self.assertEqual(tree.find(2), tree.nil)
        # This should be detached from 4's left and used as root
        self.assertEqual(tree.find(3), tree.root)

class TestRBTree(unittest.TestCase):
     
    def test_insert_with_left_rotation(self):
        tree = RBTree()
        tree.insert(1, None) # Red
        tree.insert(2, None) # Red, Parent -> Black
        tree.insert(3, None) # Red, Parent -> Rotate Left, Black, Grandparent (1) -> Red
        expected_root = tree.find(2)
        self.assertEqual(expected_root, tree.root)
        self.assertTrue(expected_root.black)
        expected_left = tree.find(1)
        self.assertEqual(expected_left, tree.root.left)
        self.assertFalse(expected_left.black)
        expected_right = tree.find(3)
        self.assertEqual(expected_right, tree.root.right)
        self.assertFalse(expected_right.black)

    def test_insert_with_right_rotation(self):
        tree = RBTree()
        tree.insert(3, None) # Red
        tree.insert(2, None) # Red, Parent -> Black
        tree.insert(1, None) # Red, Parent -> Rotate Right, Black, Grandparent (3) -> Red
        expected_root = tree.find(2)
        self.assertEqual(expected_root, tree.root)
        self.assertTrue(expected_root.black)
        expected_left = tree.find(1)
        self.assertEqual(expected_left, tree.root.left)
        self.assertFalse(expected_left.black)
        expected_right = tree.find(3)
        self.assertEqual(expected_right, tree.root.right)
        self.assertFalse(expected_right.black)
    
    def test_insert_with_left_right_rotation(self):
        tree = RBTree()
        tree.insert(9, None) # Red
        tree.insert(5, None) # Red, Parent -> Black
        tree.insert(7, None) # Red, Parent -> Rotate Right, Grandparent -> Rotate Left, then P -> Black, G -> Red
        expected_root = tree.find(7)
        self.assertEqual(expected_root, tree.root)
        self.assertTrue(expected_root.black)
        expected_left = tree.find(5)
        self.assertEqual(expected_left, tree.root.left)
        self.assertFalse(expected_left.black)
        expected_right = tree.find(9)
        self.assertEqual(expected_right, tree.root.right)
        self.assertFalse(expected_right.black)
        
    def test_insert_with_right_left_rotation(self):
        tree = RBTree()
        tree.insert(5, None) # Red
        tree.insert(9, None) # Red, Parent -> Black
        tree.insert(7, None) # Red, Parent -> Rotate Left, Grandparent -> Rotate Right, then P -> Black, G -> Red
        expected_root = tree.find(7)
        self.assertEqual(expected_root, tree.root)
        self.assertTrue(expected_root.black)
        expected_left = tree.find(5)
        self.assertEqual(expected_left, tree.root.left)
        self.assertFalse(expected_left.black)
        expected_right = tree.find(9)
        self.assertEqual(expected_right, tree.root.right)
        self.assertFalse(expected_right.black)
    
    def test_insert_with_many_imbalances(self):
        tree = RBTree()
        tree.insert(1, None) # root
        tree.insert(2, None) # balanced, recolour root -> Black
        tree.insert(3, None) # rotate left 1 (root 2), recolour 1 -> Red, 2 -> Black
        tree.insert(4, None) # balanced, recolour 1 and 3 -> Black
        tree.insert(5, None) # rotate left 3, recolour 3 -> Red, 4 -> Black
        tree.insert(6, None) # balanced, recolour 3 and 5 -> Black, 4 -> Red
        tree.insert(7, None) # rotate left 5, recolour 5 -> Red, 6 -> Black
        tree.insert(8, None) # balanced, recolour 5 and 7 -> Black, 6 -> Red, then rotate left 2 (root 4) with recolour
        tree.insert(9, None) # rotate left 7, recolour 7 -> Red, 8 -> Black
        tree.insert(10, None) # balanced, recolour 7 and 9 -> Black, 8 -> Red
        self.assertEqual(tree.find(4), tree.root)

    def test_delete_at_red_leaf(self):
        tree = RBTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)
        # red leaf
        tree.delete(10)
        expected_parent = tree.find(9)
        self.assertTrue(expected_parent.black)
        # Check no rebalance ocurred
        expected_root = tree.find(4)
        self.assertEqual(expected_root, tree.root)

    def test_delete_at_internal_node(self):
        tree = RBTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)
        # black leaf
        tree.delete(6)
        expected_parent = tree.find(4)
        self.assertTrue(expected_parent.black)
        expected_sibling = tree.find(2)
        self.assertFalse(expected_sibling.black)
        # Check that no rebalance occurred
        expected_root = tree.find(4)
        self.assertEqual(expected_root, tree.root)

    def test_delete_at_black_leaf_with_black_parent(self):
        tree = RBTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)
        # black leaf
        tree.delete(1)
        expected_parent = tree.find(2)
        self.assertTrue(expected_parent.black)
        expected_sibling = tree.find(3)
        self.assertFalse(expected_sibling.black)
        # Check that a rebalance occurred (original root was 4)
        expected_root = tree.find(6)
        self.assertEqual(expected_root, tree.root)
        # Expected change during traversal up
        self.assertTrue(expected_root.right.black)

    def test_delete_at_black_leaf_with_red_parent(self):
        tree = RBTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)
        # black leaf
        tree.delete(7)
        expected_parent = tree.find(8)
        self.assertTrue(expected_parent.black)
        expected_sibling = tree.find(9)
        self.assertFalse(expected_sibling.black)
        expected_root = tree.find(4)
        self.assertEqual(expected_root, tree.root)

    def test_delete_at_black_leaf_with_red_sibling(self):
        tree = RBTree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)
        # black leaf
        tree.delete(5)
        expected_parent = tree.find(6)
        self.assertTrue(expected_parent.black)
        expected_sibling = tree.find(7)
        self.assertFalse(expected_sibling.black)
        expected_root = tree.find(4)
        self.assertEqual(expected_root, tree.root)

class TestTreeIterator(unittest.TestCase):

    def test_iter_with_empty_tree(self):
        tree = Tree()
        list = []
        iterator = tree.iter()
        count = 0
        for item in iterator:
            count += 1
            if count >= 2:
                raise Exception("Iterator is not stopping correctly. Possible to run endlessly.")
            list.append(item.key if item is not None else None)
        self.assertSequenceEqual(list, [])

    def test_iter_with_tree_of_one(self):
        tree = Tree()
        tree.insert(1, None)
        iterator = tree.iter()
        list = []
        count = 0
        for item in iterator:
            count += 1
            if count >= 2:
                raise Exception("Iterator is not stopping correctly. Possible to run endlessly.")
            list.append(item.key if item is not None else None)
        self.assertSequenceEqual(list, [1])

    def test_iter_with_tree_of_many(self):
        tree = Tree()
        tree.insert(1, None)
        tree.insert(2, None)
        tree.insert(3, None)
        tree.insert(4, None)
        tree.insert(5, None)
        tree.insert(6, None)
        tree.insert(7, None)
        tree.insert(8, None)
        tree.insert(9, None)
        tree.insert(10, None)

        list = []
        iterator = tree.iter()
        count = 0
        for item in iterator:
            count += 1
            if count >= 11:
                raise Exception("Iterator is not stopping correctly. Possible to run endlessly.")
            list.append(item.key if item is not None else None)
        self.assertSequenceEqual(list, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

if __name__ == '__main__':
    unittest.main()