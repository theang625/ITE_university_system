import json 

def load_admins():
    with open("admins.json", "r") as f:
        return json.load(f)

def save_admins(admins):
    with open("admins.json", "w") as f:
        json.dump(admins, f, indent=4)

def main() :
# usage
    admins = load_admins()


    username = input("\nUsername: ")
    password = input("Password: ")

    admins.append({"username": username, "password": password})
    save_admins(admins)
    print(load_admins())
if __name__ == "__main__":
    
    main()