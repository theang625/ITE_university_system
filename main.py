from services.admin_service import AdminService
from utils.menu import show_admin_menu, show_main_menu, show_student_menu, login, get_admins
from data import admins


def main():
    admin_service = AdminService()
     
    print("This is the main menu of the university system.")
    while True :
        show_main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            
            print("Please enter admin username and password.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_account = login(username, password)
            if login_account: 
                return show_admin_menu()
            
        if choice == "2":
            print("Please enter student name and password")
            show_student_menu()
                        
        if choice == "3":
            print("View admin.")
            print(get_admins(), end="\n")
            
        if choice == "4":
            print("View student.")
            
        if choice == "5":
            print("Exit")
            break
        
        else: 
            print("Invalid choice, use only number for the choices.")
    
if __name__ == "__main__":
    
    main()
