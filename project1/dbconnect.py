from pymongo import MongoClient
import re
from user_menu import UserMenu

class DBConnect:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['project1']
        self.users_collection = self.db['users']
        self.counter_collection = self.db['counters']

    def get_next_sequence(self, sequence_name):
        self.counter_collection.update_one(
            {'_id': sequence_name},
            {'$inc': {'sequence_value': 1}},
            upsert=True
        )
        return self.counter_collection.find_one({'_id': sequence_name})['sequence_value']

    def validate_password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*\W).{8,}$')
        return pattern.match(password) is not None

    def create_user(self, first_name, last_name, username, password):
        if not self.validate_password(password):
            print("Password does not meet the requirements.")
            return
        
        user_id = self.get_next_sequence('user_id')
        user = {
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password
        }
        self.users_collection.insert_one(user)
        print("User created successfully.")

    def login_user(self, username, password):
        user = self.users_collection.find_one({'username': username, 'password': password})
        if user:
            print("Login successful.")
            user_id = user['id']  # Get the user_id
            user_menu = UserMenu(user_id)  # Pass user_id to UserMenu
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
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            db_connect.create_user(first_name, last_name, username, password)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
