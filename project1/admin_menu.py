from pymongo import MongoClient

class AdminMenu:
    def __init__(self, db_connect):
        self.db_connect = db_connect
        self.products_collection = self.db_connect.db['products']
        self.orders_collection = self.db_connect.db['orders']

    def display_menu(self):
        while True:
            print("\n--- Admin Menu ---")
            choice = input("Choose an option: [1] Add New Product [2] View Product [3] Edit Product [4] Delete Product [5] View all orders [6] Log out: ")
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
        
        self.products_collection.insert_one(product)
        print("Product added successfully.")

    def edit_product(self):
        self.display_products()
        product_name = input("Enter the name of the product to edit: ")
        product = self.products_collection.find_one({'item': product_name})
        
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
            
            self.products_collection.update_one({'_id': product['_id']}, {'$set': updated_product})
            print("Product updated successfully.")
        else:
            print("Product not found.")

    def delete_product(self):
        self.display_products()
        product_name = input("Enter the name of the product to delete: ")
        result = self.products_collection.delete_one({'item': product_name})
        
        if result.deleted_count > 0:
            print("Product deleted successfully.")
        else:
            print("Product not found.")

    def view_all_orders(self):
        orders = self.orders_collection.find()
        
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
        products = self.products_collection.find()
        print("\n--- Products List ---")
        for product in products:
            print(f"Name: {product['item']}, Price: ${product['price']:.2f}, Quantity: {product['quantity']}")
        print()
