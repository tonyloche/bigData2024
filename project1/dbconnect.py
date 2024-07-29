from pymongo import MongoClient
import re

class DBConnect:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['project1']
        self.users_collection = self.db['users']

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{8,}$')
        return pattern.match(password) is not None

    def create_user(self, username, password):
        if not self.validate_password(password):
            print("Password does not meet the requirements.")
            return
        
        user = {
            'username': username,
            'password': password
        }
        self.users_collection.insert_one(user)
        print("User created successfully.")

    def login_user(self, username, password):
        user = self.users_collection.find_one({'username': username, 'password': password})
        if user:
            print("Login successful.")
            user_id = user['_id']
            if str(user_id) == "66a7f1bcff3c12945d83b915":
                #print("Admin login successful.")
                from admin_menu import AdminMenu
                admin_menu = AdminMenu(self)
                admin_menu.display_menu()
            else:
                from user_menu import UserMenu 
                user_menu = UserMenu(user_id, self)
                user_menu.display_menu()
        else:
            print("Invalid username or password.")

def main():
    db_connect = DBConnect()
    
    while True:
        choice = input("Choose an option: [1] Login [2] Create New User [3] Exit: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            db_connect.login_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            db_connect.create_user(username, password)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
