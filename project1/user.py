import logging
from db_functions import DBFunctions
from admin_menu import AdminMenu
from user_menu import UserMenu
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)

class User:
    def __init__(self, db_functions, username, password):
        self.db_functions = db_functions
        self.username = username
        self.password = password
    

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{8,}$')
        is_valid = bool(pattern.match(password))
        if not is_valid:
            logging.warning(f'Password validation failed for: {password}')
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
        if self.db_functions.insert_user(user):
            print("User created successfully.")
        else:
            print("Error creating user.")

    def login_user(self):
        user = self.db_functions.find_user(self.username, self.password)
        if user:
            print("Login successful.")
            user_id = user['_id']
            logging.info(f'Login successful for username: {self.username}.')
            
            if str(user_id) == "66a7f1bcff3c12945d83b915":
                admin_menu = AdminMenu(self.db_functions)
                admin_menu.display_menu()
            else:
                user_menu = UserMenu(user_id, self.db_functions)
                user_menu.display_menu()
        else:
            print("Invalid username or password.")
            logging.warning(f'Invalid login attempt for username: {self.username}.')
