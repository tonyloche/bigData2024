import logging
from pymongo import MongoClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)

class DBFunctions:
    def __init__(self):
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['project1']
            self.users_collection = self.db['users']
            self.orders_collection = self.db['orders']
            self.products_collection = self.db['products']
            logging.info('Connected to MongoDB successfully.')
        except Exception as e:
            logging.error(f'Error connecting to MongoDB: {e}')

    def insert_user(self, user):
        try:
            self.users_collection.insert_one(user)
            logging.info(f'User created successfully with username: {user["username"]}.')
            return True
        except Exception as e:
            logging.error(f'Error creating user: {e}')
            return False

    def find_user(self, username, password):
        try:
            user = self.users_collection.find_one({'username': username, 'password': password})
            return user
        except Exception as e:
            logging.error(f'Error finding user: {e}')
            return None

    def count_user_orders(self, user_id):
        try:
            return self.orders_collection.count_documents({'user_id': user_id})
        except Exception as e:
            logging.error(f'Error counting user orders: {e}')
            return 0

    def find_user_orders(self, user_id):
        try:
            return self.orders_collection.find({'user_id': user_id})
        except Exception as e:
            logging.error(f'Error finding user orders: {e}')
            return []

    def insert_product(self, product):
        try:
            self.products_collection.insert_one(product)
            logging.info(f'Product added successfully: {product["item"]}.')
            return True
        except Exception as e:
            logging.error(f'Error adding product: {e}')
            return False

    def find_product_by_name(self, name):
        try:
            return self.products_collection.find_one({'item': name})
        except Exception as e:
            logging.error(f'Error finding product by name: {e}')
            return None

    def update_product(self, product_id, updated_product):
        try:
            self.products_collection.update_one({'_id': product_id}, {'$set': updated_product})
            logging.info(f'Product updated successfully: {updated_product["item"]}.')
            return True
        except Exception as e:
            logging.error(f'Error updating product: {e}')
            return False

    def delete_product_by_name(self, name):
        try:
            result = self.products_collection.delete_one({'item': name})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f'Error deleting product by name: {e}')
            return False

    def find_all_orders(self):
        try:
            return self.orders_collection.find()
        except Exception as e:
            logging.error(f'Error finding all orders: {e}')
            return []

    def find_all_products(self):
        try:
            return self.products_collection.find()
        except Exception as e:
            logging.error(f'Error finding all products: {e}')
            return []

    def find_all_users(self):
        try:
            return self.users_collection.find()
        except Exception as e:
            logging.error(f'Error finding all users: {e}')
            return []
