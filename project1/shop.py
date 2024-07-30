from datetime import datetime

class Shop:
    def __init__(self, user_id, db_functions):
        self.user_id = user_id
        self.db_functions = db_functions
        self.cart = []

    def display_products(self):
        products = self.db_functions.products_collection.find()
        print("\n--- Products List ---")
        for index, product in enumerate(products):
            print(f"{index + 1}. {product['item']} - ${product['price']:.2f}")
            print(f"   Stock: {product['quantity']}")
        print()

    def choose_product(self):
        self.display_products()
        try:
            choice = int(input("Enter the number of the product you want to buy: ")) - 1
            product = self.db_functions.products_collection.find().skip(choice).limit(1).next()
            if not product:
                print("Invalid choice. Product not found.")
                return
            
            quantity = int(input("Enter quantity to add to cart: "))
            if quantity <= 0 or quantity > product['quantity']:
                print("Invalid quantity. Must be between 1 and available stock.")
                return
            
            self.cart.append({
                'item': product['item'],
                'price': product['price'],
                'quantity': quantity
            })
            print(f"Added {quantity} {product['item']}(s) to cart.")
        
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    def display_cart(self):
        if not self.cart:
            print("Your cart is empty.")
            return None
        
        print("\n--- Cart Summary ---")
        total_price = 0
        for index, item in enumerate(self.cart):
            item_total = item['price'] * item['quantity']
            total_price += item_total
            print(f"{index + 1}. {item['quantity']} x {item['item']} - ${item['price']:.2f} each - Total: ${item_total:.2f}")
        print(f"Total Price: ${total_price:.2f}")
        print()
        return total_price
    
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
                elif action == '2':
                    del self.cart[choice]
                    print("Item removed.")
                else:
                    print("Invalid action.")
            except ValueError:
                print("Invalid input.")

    def update_products(self):
        for item in self.cart:
            query = {'item': item['item']}
            product = self.db_functions.products_collection.find_one(query)
            if product:
                new_quantity = product['quantity'] - item['quantity']
                if new_quantity < 0:
                    print(f"Not enough stock for {item['item']}.")
                    continue  # Skip updating if there's not enough stock
                
                self.db_functions.products_collection.update_one(
                    {'_id': product['_id']},
                    {'$set': {'quantity': new_quantity}}
                )
            else:
                print(f"Product {item['item']} not found.")

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
            # Insert the new order
            self.db_functions.orders_collection.insert_one(purchase)
            print("Thank you for your purchase!")
            print(f"Total: ${total_price:.2f}")
            self.update_products()
            # Clear the cart after checkout
            self.cart = [] 
        else:
            print("Checkout canceled.")
