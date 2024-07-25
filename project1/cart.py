from pymongo import MongoClient
from datetime import datetime

class Cart:
    def __init__(self, user_id, cart_contents):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['project1']
        self.cart_collection = self.db['orders']
        self.products_collection = self.db['products']
        self.user_id = user_id
        self.cart = cart_contents

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
                elif action == '2':
                    del self.cart[choice]
                    print("Item removed.")
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
            self.cart_collection.insert_one(purchase)
            print("Thank you for your purchase!")
            print(f"Total: ${total_price:.2f}")
            self.update_products()
            self.cart = []  # Clear the cart after checkout
        else:
            print("Checkout canceled.")

def main():
    # Example usage:
    user_id = 1  # Replace with actual user ID
    cart_contents = [
        {'name': 'T-shirt', 'price': 9.99, 'size': 'M', 'quantity': 2},
        {'name': 'Jeans', 'price': 29.99, 'size': 'L', 'quantity': 1}
    ]
    
    cart = Cart(user_id, cart_contents)
    while True:
        print("\n--- Cart Menu ---")
        action = input("Choose an option: [1] View Cart [2] Modify Cart [3] Checkout [4] Back to Shop: ")
        if action == '1':
            cart.display_cart()
        elif action == '2':
            cart.modify_cart()
        elif action == '3':
            cart.checkout()
        elif action == '4':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
