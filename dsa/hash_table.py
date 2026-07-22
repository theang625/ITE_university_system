import math

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
    def __init__(self, size = 20):
        self.size = size
        self.buckets = [[] for _ in range(self.size)]  # list of lists (chaining)
        self.count = 0

    def _hash(self, key):
        """Convert key into an index within bucket range."""
        A = 0.6180339887
        return math.floor(self.size * ((int(key) * A) % 1))

    def insertion(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # If key already exists, update its value
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Otherwise, add new entry
        bucket.append((key, value))
        self.count += 1

        # Resize if load factor gets too high (keeps lookups fast)
        if self.count / self.size > 0.75:
            self._resize()

    def get(self, key):
        """Return the value for a key, or None if not found."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Remove a key-value pair. Returns True if deleted, False if not found."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                
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

    def contains(self, key):
        """Check if a key exists."""
        return self.get(key) is not None

    def keys(self):
        """Return all keys stored."""
        return [k for bucket in self.buckets for k, v in bucket]

    def values(self):
        """Return all values stored."""
        return [v for bucket in self.buckets for k, v in bucket]

    def items(self):
        """Return all (key, value) pairs."""
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def _resize(self):
        """Double the bucket count and reinsert all items (keeps lookups O(1))."""
        old_items = self.items()
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for k, v in old_items:
            self.insertion(k, v)

    def __len__(self):
        return self.count

    def __repr__(self):
        return f"HashTable({self.items()})"
    
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
