from datetime import datetime
from pymongo import MongoClient

class Shop:
    def __init__(self, user_id, db_connect):
        self.user_id = user_id
        self.db_connect = db_connect
        self.products_collection = self.db_connect.db['products']
        self.cart_collection = self.db_connect.db['orders']
        self.cart = []
        self.load_cart()

    def load_cart(self):
        # Load cart items from the database if they exist
        cart_order = self.cart_collection.find_one({'user_id': self.user_id, 'status': 'pending'})
        if cart_order:
            self.cart = cart_order.get('items', [])
        else:
            self.cart = []

    def save_cart(self):
        # Save the current cart to the database if it's not empty
        if self.cart:
            self.cart_collection.update_one(
                {'user_id': self.user_id, 'status': 'pending'},
                {'$set': {'items': self.cart}},
                upsert=True
            )
        else:
            # If the cart is empty, remove any pending orders
            self.cart_collection.delete_one({'user_id': self.user_id, 'status': 'pending'})

    def display_products(self):
        products = self.products_collection.find()
        print("\n--- Products List ---")
        for index, product in enumerate(products):
            print(f"{index + 1}. {product['name']} - ${product['price']:.2f}")
            if 'size' in product and product['size']:
                print(f"   Available Sizes: {', '.join(product['size'])}")
            print(f"   Stock: {product['stock']}")
        print()

    def choose_product(self):
        self.display_products()
        try:
            choice = int(input("Enter the number of the product you want to buy: ")) - 1
            product = self.products_collection.find().skip(choice).limit(1).next()
            if not product:
                print("Invalid choice. Product not found.")
                return
            
            size = None
            if 'size' in product and product['size']:
                size = input(f"Choose a size from {', '.join(product['size'])}: ")
                if size not in product['size']:
                    print("Invalid size choice.")
                    return
            
            quantity = int(input("Enter quantity to add to cart: "))
            if quantity <= 0 or quantity > product['stock']:
                print("Invalid quantity. Must be between 1 and available stock.")
                return
            
            self.cart.append({
                'name': product['name'],
                'price': product['price'],
                'size': size,
                'quantity': quantity
            })
            print(f"Added {quantity} of {product['name']} to cart.")
            self.save_cart()
        
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    def display_cart(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        
        print("\n--- Cart Summary ---")
        total_price = 0
        for index, item in enumerate(self.cart):
            item_total = item['price'] * item['quantity']
            total_price += item_total
            print(f"{index + 1}. {item['quantity']} x {item['name']} ({item['size'] if item['size'] else 'No Size'}) - ${item['price']:.2f} each - Total: ${item_total:.2f}")
        print(f"Total Price: ${total_price:.2f}")
        print()
        return total_price
    
    def update_products(self):
        for item in self.cart:
            query = {'name': item['name']}
            if item['size']:
                query['size'] = item['size']
            
            product = self.products_collection.find_one(query)
            if product:
                new_stock = product['stock'] - item['quantity']
                if new_stock < 0:
                    print(f"Not enough stock for {item['name']} ({item['size'] if item['size'] else 'No Size'}).")
                    continue  # Skip updating this item if there's not enough stock
                
                self.products_collection.update_one(
                    {'_id': product['_id']},
                    {'$set': {'stock': new_stock}}
                )
            else:
                print(f"Product {item['name']} ({item['size'] if item['size'] else 'No Size'}) not found.")

    def modify_cart(self):
        while True:
            self.display_cart()
            try:
                choice = int(input("Enter the number of the item to modify/remove or [0] to go back: ")) - 1
                if choice == -1:
                    break
                if choice < 0 or choice >= len(self.cart):
                    print("Invalid choice.")
                    continue
                
                action = input("Enter [1] to change quantity, [2] to remove item: ")
                if action == '1':
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be greater than 0.")
                    else:
                        self.cart[choice]['quantity'] = new_quantity
                        print("Quantity updated.")
                        self.save_cart()
                elif action == '2':
                    del self.cart[choice]
                    print("Item removed.")
                    self.save_cart()
                else:
                    print("Invalid action.")
            except ValueError:
                print("Invalid input.")

    def checkout(self):
        total_price = self.display_cart()
        if total_price is None:
            return
        
        confirm = input("Confirm checkout? [Y/N]: ")
        if confirm.lower() == 'y':
            # Save purchase details to MongoDB
            purchase = {
                'user_id': self.user_id,
                'date_time': datetime.now(),
                'items': self.cart,
                'total_price': total_price
            }
            # Remove any pending cart items for this user
            self.cart_collection.delete_one({'user_id': self.user_id, 'status': 'pending'})
            # Insert the new order
            self.cart_collection.insert_one(purchase)
            print("Thank you for your purchase!")
            print(f"Total: ${total_price:.2f}")
            self.update_products()
            self.cart = []  # Clear the cart after checkout
            self.save_cart()  # Save empty cart state
        else:
            print("Checkout canceled.")
