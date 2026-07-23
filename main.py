from utils.menu import show_admin_menu, show_main_menu, show_student_menu, login, get_admins, get_student
import json

def main():
     
    print("This is the main menu of the university system.")
    while True :
        
        show_main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            
            print("Please enter admin username and password.")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
           
            login_account = login(username, password)
            if not login_account: 
                return show_main_menu()
            
        elif choice == "2":
            print("Please enter student name and password")
            show_student_menu()
            
        elif choice == "3":
            print("View student.")
            print("=" * 35)
            print(get_student())
            
        elif choice == "4":
            print("Exit")
            break
        
        else:
            print("Invalid choice")
                  
if __name__ == "__main__":
    
    main()
