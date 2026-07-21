class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node((key, value))
            return

        current = self.root
        while True:
            
            if key == current.value[0]:
                current.value = (key, value)
                return
            elif key < current.value[0]:
                if current.left is None:
                    current.left = Node((key, value))
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node((key, value))
                    return
                current = current.right

    def search(self, key):
        """Searches for a key in the binary tree with safe type matching."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current, key):
        if current is None:
            return None

        node_key = current.value[0]

        # ព្យាយាមប្រៀបធៀបដោយផ្ទាល់ បើខុស Type គ្នា ត្រូវប្តូរទៅជា String ដូចគ្នាដើម្បីការពារ TypeError
        try:
            if key == node_key:
                return current.value[1]
            elif key < node_key:
                return self._search_recursive(current.left, key)
            else:
                return self._search_recursive(current.right, key)
        except TypeError:
            # ករណី Type មិនត្រូវគ្នា (str vs int) គឺប្តូរវាទៅជា string ទាំងអស់ដើម្បីប្រៀបធៀបបន្ត
            str_key = str(key)
            str_node_key = str(node_key)
            if str_key == str_node_key:
                return current.value[1]
            elif str_key < str_node_key:
                return self._search_recursive(current.left, key)
            else:
                return self._search_recursive(current.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)

    def remove(self, key):
        self.root = self._remove(self.root, key)

    def _remove(self, node, key):
        if node is None:
            return None
        if key < node.value[0]:
            node.left = self._remove(node.left, key)
        elif key > node.value[0]:
            node.right = self._remove(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._remove(node.right, min_node.value[0])
        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
