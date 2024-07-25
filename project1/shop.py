from pymongo import MongoClient
from cart import Cart  # Import the Cart class

class Shop:
    def __init__(self, user_id):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['project1']
        self.products_collection = self.db['products']
        self.cart = []
        self.user_id = user_id

    def display_products(self):
        products = self.products_collection.find()
        print("\n--- Products List ---")
        for index, product in enumerate(products):
            print(f"{index + 1}. {product['name']} - ${product['price']:.2f}")
            if product['size']:
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
            
            if product['size']:
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
                'size': size if product['size'] else None,
                'quantity': quantity
            })
            print(f"Added {quantity} of {product['name']} to cart.")
        
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    def view_cart_checkout(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        
        # Pass the cart contents to the Cart class
        cart_instance = Cart(self.user_id, self.cart)
        
        while True:
            print("\n--- Cart Menu ---")
            action = input("Choose an option: [1] View Cart [2] Modify Cart [3] Checkout [4] Back to Shop: ")
            if action == '1':
                cart_instance.display_cart()
            elif action == '2':
                cart_instance.modify_cart()
            elif action == '3':
                cart_instance.checkout()
                # Optionally clear the cart after checkout
                self.cart = cart_instance.cart
                break
            elif action == '4':
                break
            else:
                print("Invalid choice. Please select again.")

def main():
    user_id = 1  # Replace with actual user ID logic
    shop = Shop(user_id)
    
    while True:
        print("\n--- Shop Menu ---")
        choice = input("Choose an option: [1] Shop [2] View Cart/Checkout [3] Exit: ")
        if choice == '1':
            shop.choose_product()
        elif choice == '2':
            shop.view_cart_checkout()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
