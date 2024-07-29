import logging
import re
from pymongo import MongoClient

# Setup logging configuration
logging.basicConfig(filename='db_connect.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DBConnect:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['project1']
            self.users_collection = self.db['users']
            logging.info('Connected to MongoDB and selected database.')
        except Exception as e:
            logging.error(f'Error connecting to MongoDB: {e}')

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{8,}$')
        is_valid = pattern.match(password) is not None
        if not is_valid:
            logging.warning(f'Password validation failed for password: {password}')
        return is_valid

    def create_user(self, username, password):
        if not self.validate_password(password):
            print("Password does not meet the requirements.")
            logging.info(f'User creation failed for username: {username}. Password does not meet requirements.')
            return
        
        user = {
            'username': username,
            'password': password
        }
        try:
            self.users_collection.insert_one(user)
            print("User created successfully.")
            logging.info(f'User created successfully with username: {username}.')
        except Exception as e:
            logging.error(f'Error creating user: {e}')

    def login_user(self, username, password):
        try:
            user = self.users_collection.find_one({'username': username, 'password': password})
            if user:
                print("Login successful.")
                user_id = user['_id']
                logging.info(f'Login successful for username: {username}.')
                
                if str(user_id) == "66a7f1bcff3c12945d83b915":
                    from admin_menu import AdminMenu
                    admin_menu = AdminMenu(self)
                    admin_menu.display_menu()
                else:
                    from user_menu import UserMenu
                    user_menu = UserMenu(user_id, self)
                    user_menu.display_menu()
            else:
                print("Invalid username or password.")
                logging.warning(f'Invalid login attempt for username: {username}.')
        except Exception as e:
            logging.error(f'Error during login: {e}')

def main():
    db_connect = DBConnect()
    
    while True:
        print("Welcome to Bob's Burgers and More")
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
            logging.info('User exited the application.')
            break
        else:
            print("Invalid choice. Please select again.")
            logging.warning('Invalid menu choice.')

if __name__ == "__main__":
    main()
