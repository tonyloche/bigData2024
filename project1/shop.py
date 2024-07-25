from pymongo import MongoClient

class Shop:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['project1']
        self.products_collection = self.db['products']
        self.cart = []

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
        
        print("\n--- Cart Summary ---")
        for item in self.cart:
            print(f"{item['quantity']} x {item['name']} ({item['size'] if item['size'] else 'No Size'}) - ${item['price']:.2f} each")
        print()
        print("Prepare to send this information to the next class...")
        # This is where you would call the next class to handle checkout

def main():
    shop = Shop()
    
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
