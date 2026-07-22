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