
import json
import math
import os
from services import admin_service
"""
hash_table.py
Hash Table logic for fast student lookup by student_id.
Solves: slow searching student info by id.

Uses multiplicative hashing with chaining (list of buckets, each bucket is
a list of student dicts that hashed to the same index).
"""

import math

class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(size)]

    # ----------------------------
    # Hash Function
    # ----------------------------
    def _hash(self, key):
        A = 0.6180339887
        return math.floor(self.size * ((int(key) * A) % 1))

    # ----------------------------
    # Insert Student
    # ----------------------------
    def insert(self, student):
        
        key = student["id"]
        index = self._hash(key)

        # Update if already exists
        for item in self.table[index]:
            if item["id"] == key:
                item.update(student)
                return

        self.table[index].append(student)

    # ----------------------------
    # Search Student
    # ----------------------------
    def get(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item["id"] == key:
                return item

        return None

    # ----------------------------
    # Delete Student
    # ----------------------------
    def delete(self, key):
        index = self._hash(key)

        for item in self.table[index]:
            if item["id"] == key:
                self.table[index].remove(item)
    def multiplication_hash(self, student_id):
        """Multiplicative hashing: maps student_id to a bucket index 0..size-1."""
        M = self.size
        A = 0.618033  # golden ratio conjugate - common choice for this method
        return math.floor(M * ((student_id * A) % 1))

    def insert(self, student_id, name, email, year, gpa):
        """Insert a new student. Rejects duplicates by student_id (not name -
        two students CAN share a name, they can't share a student_id)."""
        index = self.multiplication_hash(student_id)

        for info in self.table[index]:
            if info["student_id"] == student_id:
                print("Student already exists!")
                return None

        info = {
            "student_id": student_id,
            "name": name,
            "email": email,
            "year": year,
            "gpa": gpa,
        }

    def find(self, student_id):
        """O(1)-ish lookup by student_id. Returns the student dict or None."""
        index = self.multiplication_hash(student_id)
        for info in self.table[index]:
            if info["student_id"] == student_id:
                return info
        return None

    def delete(self, student_id):
        """Remove a student entry. Returns True if deleted, False if not found."""
        index = self.multiplication_hash(student_id)
        for info in self.table[index]:
            if info["student_id"] == student_id:
                self.table[index].remove(info)
                return True

        return False

    # ----------------------------
    # Update Student
    # ----------------------------
    def update(self, key, **kwargs):
        student = self.get(key)

        if student:
            student.update(kwargs)
            return True

        return False

    # ----------------------------
    # Return all students
    # ----------------------------
    def values(self):
        students = []

        for bucket in self.table:
            students.extend(bucket)

        return students

    # ----------------------------
    # Load JSON File
    # ----------------------------
    def load_json(self, filename):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for student in data:
            self.insert(student)

    # ----------------------------
    # Save JSON File
    # ----------------------------
    def save_json(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.values(), file, indent=4)

    def update(self, student_id, name=None, email=None, year=None, gpa=None):
        """Update fields on an existing student. Returns the updated dict or None."""
        student = self.find(student_id)
        if student is None:
            return None
        if name is not None:
            student["name"] = name
        if email is not None:
            student["email"] = email
        if year is not None:
            student["year"] = year
        if gpa is not None:
            student["gpa"] = gpa
        return student

    def exists(self, student_id):
        """Check if a student_id is already in the table."""
        return self.find(student_id) is not None

    def values(self):
        """Return all students currently in the table, as a flat list."""
        result = []
        for bucket in self.table:
            for info in bucket:
                result.append(info)
        return result
