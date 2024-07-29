from shop import Shop

class UserMenu:
    def __init__(self, user_id, db_connect):
        self.user_id = user_id
        self.db_connect = db_connect
        self.shop = Shop(self.user_id, self.db_connect.db)  # Create a single instance of Shop

    def display_menu(self):
        while True:
            print("\n--- User Menu ---")
            choice = input("Choose an option: [1] Shop [2] View Cart/Checkout [3] View Orders [4] Logout: ")
            if choice == '1':
                self.shop.choose_product()  # Use the existing shop instance
            elif choice == '2':
                self.shop.display_cart() 
                self.modify_cart() 
            elif choice == '3':
                self.view_orders()
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please select again.")

    def modify_cart(self):
        while True:
            print("\n--- Cart Menu ---")
            action = input("Choose an option: [1] Modify Cart [2] Checkout [3] Back to Menu: ")
            if action == '1':
                self.shop.modify_cart()
            elif action == '2':
                self.shop.checkout()
                break  # Exit cart menu after checkout
            elif action == '3':
                break
            else:
                print("Invalid choice. Please select again.")
    
    def view_orders(self):
        orders_collection = self.db_connect.db['orders']
        order_count = orders_collection.count_documents({'user_id': self.user_id})

        if order_count == 0:
            print("No orders found.")
            return

        orders = orders_collection.find({'user_id': self.user_id})

        print("\n--- Orders ---")
        for order in orders:
            print(f"Date: {order['date_time']}")
            print(f"Total Price: ${order['total_price']:.2f}")
            for item in order['items']:
                print(f"  - {item['quantity']} x {item['item']} ${item['price']:.2f}")
            print()

