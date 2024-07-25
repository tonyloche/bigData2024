from shop import Shop

class UserMenu:
    def __init__(self, user_id):
        self.user_id = user_id
        self.shop = Shop(user_id)  # Pass user_id to Shop

    def display_menu(self):
        while True:
            print("\n--- User Menu ---")
            choice = input("Choose an option: [1] Shop [2] View Cart/Checkout [3] View Orders [4] Logout: ")
            if choice == '1':
                self.shop_menu()
            elif choice == '2':
                self.view_cart_checkout()
            elif choice == '3':
                self.view_orders()
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please select again.")

    def shop_menu(self):
        self.shop.choose_product()

    def view_cart_checkout(self):
        self.shop.view_cart_checkout()
    
    def view_orders(self):
        print("View orders functionality will be implemented here.")
