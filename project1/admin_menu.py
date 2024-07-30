import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log')
    ]
)

class AdminMenu:
    def __init__(self, db_functions):
        self.db_functions = db_functions

    def display_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            choice = input("Choose an option: [1] Add New Product [2] View Products [3] Edit Product [4] Delete Product [5] View All Orders [6] View All Users [7] Log Out: ")
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '3':
                self.edit_product()
            elif choice == '4':
                self.delete_product()
            elif choice == '5':
                self.view_all_orders()
            elif choice == '6':
                self.display_all_users()
            elif choice == '7':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please select again.")

    def view_products(self):
        self.display_products()

    def add_product(self):
        item = input("Enter product name: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        
        product = {
            'item': item,
            'price': price,
            'quantity': quantity
        }
        
        if self.db_functions.insert_product(product):
            print("Product added successfully.")
            logging.info(f'Product added: {item}.') 
        else:
            print("Failed to add product.")

    def edit_product(self):
        self.display_products()
        product_name = input("Enter the name of the product to edit: ")
        product = self.db_functions.find_product_by_name(product_name)
        
        if product:
            print("Leave field blank to keep current value.")
            new_item = input(f"Enter new name (current: {product['item']}): ") or product['item']
            new_price = input(f"Enter new price (current: {product['price']}): ") or product['price']
            new_quantity = input(f"Enter new quantity (current: {product['quantity']}): ") or product['quantity']
            
            updated_product = {
                'item': new_item,
                'price': float(new_price),
                'quantity': int(new_quantity)
            }
            
            if self.db_functions.update_product(product['_id'], updated_product):
                print("Product updated successfully.")
                logging.info(f'Product updated: {product_name}.')
            else:
                print("Failed to update product.")
        else:
            print("Product not found.")

    def delete_product(self):
        self.display_products()
        product_name = input("Enter the name of the product to delete: ")
        if self.db_functions.delete_product_by_name(product_name):
            print("Product deleted successfully.")
            logging.info(f'Product deleted: {product_name}.')
        else:
            print("Product not found.")

    def view_all_orders(self):
        orders = self.db_functions.find_all_orders()
        
        print("\n--- All Orders ---")
        for order in orders:
            print(f"Order ID: {order['_id']}")
            print(f"User ID: {order['user_id']}")
            print(f"Date: {order['date_time']}")
            print(f"Total Price: ${order['total_price']:.2f}")
            for item in order['items']:
                print(f"  - {item['quantity']} x {item['item']} x ${item['price']:.2f}")
            print()

    def display_products(self):
        products = self.db_functions.find_all_products()
        print("\n--- Products List ---")
        for product in products:
            print(f"Name: {product['item']}, Price: ${product['price']:.2f}, Quantity: {product['quantity']}")
        print()
    
    def display_all_users(self):
        users = self.db_functions.find_all_users()
        print("\n--- All Users ---")
        for user in users:
            print(f"Username: {user['username']}")
        print()
