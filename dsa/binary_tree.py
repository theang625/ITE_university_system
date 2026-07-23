import json
import os


class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
class BinaryTree:
    def __init__(self):
        self.root = None

    # ---------- INSERT ----------
    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return TreeNode(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value

        return node

    # ---------- SEARCH ----------
    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # ---------- REMOVE ----------
    def remove(self, key):
        self.root, removed = self._remove(self.root, key)
        return removed

    def _remove(self, node, key):
        if node is None:
            return node, False

        if key < node.key:
            node.left, removed = self._remove(node.left, key)
        elif key > node.key:
            node.right, removed = self._remove(node.right, key)
        else:
            removed = True
            if node.left is None:
                return node.right, removed
            if node.right is None:
                return node.left, removed

            successor = node.right
            while successor.left:
                successor = successor.left

            node.key = successor.key
            node.value = successor.value
            node.right, _ = self._remove(node.right, successor.key)

        return node, removed

    # ---------- TRAVERSAL ----------
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)
            
    def reverse_inorder(self):
        """Returns list of (key, value) pairs sorted by key DESCENDING (right -> node -> left)."""
        result = []
        self._reverse_inorder(self.root, result)
        return result

    def _reverse_inorder(self, node, result):
        if node:
            self._reverse_inorder(node.right, result)   # right first = bigger values first
            result.append((node.key, node.value))
            self._reverse_inorder(node.left, result)

    # ---------- LOAD FROM JSON ----------
    def load_from_json(self, file_path, key_field):
        """
        Reads a JSON file (a list of dicts) and inserts each item into the
        tree one by one, using item[key_field] as the sort key.
        Example: tree.load_from_json("courses.json", "course_id")
        """
        if not os.path.exists(file_path):
            print(f"{file_path} not found. Starting with an empty tree.")
            return

        with open(file_path, "r") as f:
            data = json.load(f)

        for item in data:
            key = item[key_field]
            self.insert(key, item)   # insert one at a time

        print(f"Loaded {len(data)} items from {file_path} into the tree.")

    def __len__(self):
        return len(self.inorder())