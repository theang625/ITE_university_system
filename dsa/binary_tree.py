from fileinput import filename
import json

from models import student


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
            if key < current.value[0]:
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
        current = self.root
        while current is not None:
            if key == current.value[0]:
                return current.value[1]
            if key < current.value[0]:
                current = current.left
            else:
                current = current.right
        return None

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

    def _find_min(self, node): #tree clean
        current = node
        while current.left is not None:
            current = current.left
        return current
    def load_students_from_json(tree, filename="students.json"):
        # Clear the old tree
        tree.root = None

        with open(filename, "r") as file:
            students = json.load(file)

        for student in students:
            # Change "student_id" if your JSON uses another key
            tree.insert(student["student_id"], student)

        print(f"{len(students)} students loaded into Binary Tree.")
        def print_student(student):
            if student is None:
                print("Student not found.")
            return

            print("\n===== Student Information =====")
            print(f"ID      : {student['student_id']}")
            print(f"Name    : {student['name']}")
            print(f"Gender  : {student['gender']}")
            print(f"Age     : {student['age']}")
            print(f"Major   : {student['major']}")
            print(f"Year    : {student['year']}")
            print(f"GPA     : {student['gpa']}")
            print(f"Email   : {student['email']}")
            print(f"Phone   : {student['phone']}")
        def search_student(tree):
            student_id = int(input("Enter Student ID: "))

            student = tree.search(student_id)
            
            print_student(student)
        def print_all_students(tree):
            print("\n===== Student List =====")

            for key, student in tree.inorder():
                print(f"{student['student_id']} | {student['name']} | GPA: {student['gpa']}")