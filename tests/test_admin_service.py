import json 

def load_admins():
    with open("students.json", "r") as f:
        return json.load(f)

def save_admins(students):
    with open("students.json", "w") as f:
        json.dump(students, f, indent=5)

def main() :
# usage
    students = load_admins()


    user_id = input("id: ")
    name = input("name: ")
    email = input("Email: ")
    year = input("Year: ")
    gpa = input("GPA: ")

    students.append({"id": user_id, "username": name, "email": email, "year": year, "gpa": gpa})
    save_admins(students)
    print(load_admins())
if __name__ == "__main__":
    
    main()