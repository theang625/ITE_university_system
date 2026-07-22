import json
import os
class Admin:
    def __init__(self, admin_id, name, email):
        self.admin_id = admin_id
        self.name = name

    def __repr__(self):
        return f"Admin({self.admin_id}, {self.name}, {self.email})"
    
    def get_admins() :
    
        with open("admins.json", "r") as f:
            admins = json.load(f)
        for admin in admins:
            print(f"Username: {admin['username']}")
            
    def load_admins():
        if not os.path.exists("admins.json"):
            return []
        with open("admins.json", "r") as f:
            return json.load(f)
