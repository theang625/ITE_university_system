import math
import json
from models.student import Student

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def multiplication_hash(self, phone):
        # M is the size of the hash table
        M = self.size 
        
        # A is a constant (The Golden Ratio conjugate is a common choice)
        A = 0.618033 
    
        # Take the floor of the result to get an integer index
        hash_value = math.floor(M * ((phone * A) % 1))
        
        return hash_value

    def student_insert(self, user_id, name, email, gpa):
        
        # Get the index for this phone number
        index = self.multiplication_hash(user_id)
        
        # Check if the phone number already exists in this bucket
        for imformation in self.table[index]:
            if imformation["name"] == name:
                print("User already exists!")
                return
                
        # Create a new contact dictionary
        imformation = {
            "user_id" : id,
            "name": name,
            "phone": email,
            "gpa" : gpa
        }
                
        # Add the contact to the bucket (Chaining)
        self.table[index].append(imformation)
        print(f"Insertion: [{user_id}, {name} -> {email}]")

    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                self.table[index].remove(item)
                return True
        return False

    def values(self):
        values = []
        for bucket in self.table:
            for _, value in bucket:
                values.append(value)
        return values

    def print_table(self):
        for i, bucket in enumerate(self.table):
            print(f"Bucket {i}: {bucket}")