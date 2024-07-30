from user import User
from db_functions import DBFunctions

def main():
    db_functions = DBFunctions()
    while True:
        choice = input("Choose an option: [1] Login [2] Create New User [3] Exit: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(db_functions, username, password)
            user.login_user()
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(db_functions, username, password)
            user.create_user(username, password)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
