import math
import json
import os


class HashTable:
    def __init__(self, size=20):
        self.size = size
        self.buckets = [[] for _ in range(self.size)]  # list of lists (chaining)
        self.count = 0

    def _hash(self, key):
        """Convert key into an index within bucket range using multiplication hashing."""
        A = 0.6180339887

        # Support both int keys (e.g. 8) and string keys (e.g. "S008")
        if isinstance(key, int):
            numeric_key = key
        else:
            numeric_key = sum(ord(char) for char in str(key))  # turn string into a number

        return math.floor(self.size * ((numeric_key * A) % 1))

    def insertion(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

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
                return True
        return False

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        return [k for bucket in self.buckets for k, v in bucket]

    def values(self):
        return [v for bucket in self.buckets for k, v in bucket]

    def items(self):
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def _resize(self):
        old_items = self.items()
        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0
        for k, v in old_items:
            self.insertion(k, v)

    # ---------- LOAD FROM JSON ----------
    def load_from_json(self, file_path, key_field):
        """
        Reads a JSON file (a list of dicts) and inserts each item into the
        hash table one by one, using item[key_field] as the key.
        Example: table.load_from_json("students.json", "student_id")
        """
        if not os.path.exists(file_path):
            print(f"{file_path} not found. Starting with an empty hash table.")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            key = item[key_field]
            self.insertion(key, item)   # insert one at a time

        print(f"Loaded {len(data)} items from {file_path} into the hash table.")

    def __len__(self):
        return self.count

    def __repr__(self):
        return f"HashTable({self.items()})"