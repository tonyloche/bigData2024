import csv
from datetime import datetime

def main():
    file_name = 'food_inventory.csv'
    inventory = read_csv(file_name)
    while True:
        print("Menu:")
        print(" [A] Add food")
        print(" [D] Delete food")
        print(" [I] Inventory")
        print(" [O] Order food")
        print(" [R] Read receipts")
        print(" [U] Update")
        print(" [Q] Quit")
        command = input("\nPlease select an option: ").lower()
        if command == 'i':
            display_inventory(inventory)
        elif command == 'a':
            add_food(inventory)
        elif command == 'd':
            delete_food(inventory)
        elif command == 'o':
            order_food(inventory)
        elif command == 'r':
            read_receipt()
        elif command == 'u':
            update_inventory(inventory)
        elif command == 'q':
            write_csv(file_name, inventory)
            print("Changes saved to file. Exiting.")
            break
        else:
            print("Invalid input")

def read_csv(file_name):
    inventory = []
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            inventory.append(row)
    return inventory

def write_csv(file_name, inventory):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(inventory)

def write_receipt(food, price, quantity, total):
    with open('receipts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d,%H:%M:%S")
        writer.writerow([date_time.split(",")[0], date_time.split(",")[1], food, price, quantity, total])

def read_receipt(): 
    with open('receipts.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def display_inventory(inventory):

    col1_width = max(len(item[0]) for item in inventory) + 2
    col2_width = max(len(str(item[1])) for item in inventory) + 2
    col3_width = max(len(str(item[2])) for item in inventory) + 2
    print("\nCurrent Inventory:")
    for item in inventory:
        print(f"{item[0].ljust(col1_width)}{str(item[1]).ljust(col2_width)}{str(item[2]).ljust(col3_width)}")
        print("-" * (col1_width + col2_width + col3_width))
    print()

def add_food(inventory):
    item_name = input("Enter the item name to add: ")
    price = input(f"Enter the price for {item_name}: ")
    quantity = input(f"Enter the quantity for {item_name}: ")
    inventory.append([item_name, price, quantity])
    print(f"{item_name} added successfully.")

def order_food(inventory):
    display_inventory(inventory)
    item_name = input("Enter the item name to order: ")
    for item in inventory:
        if item[0] == item_name and int(item[2] == 0):
            print(f"{item_name} is out of stock.")
            return
        elif item[0] == item_name:
            quantity = int(input(f"Enter the quantity of {item_name} to order: "))
            if quantity > int(item[2]):
                print(f"Only {item[2]} {item_name} in stock. Order failed.")
                return
            item[2] = str(int(item[2]) - quantity)
            total_price = float(item[1]) * quantity
            print(f"{quantity} {item_name} ordered successfully.")
            print(f"total price: {float(item[1]) * quantity}")
            write_receipt(item_name, item[1], quantity, total_price)
            return
    print(f"{item_name} not found in inventory.")

def update_inventory(inventory):
    display_inventory(inventory)
    item_name = input("Enter the item name to update: ")
    for item in inventory:
        if item[0] == item_name:
            item[1] = input(f"Enter new price for {item_name}: ")
            item[2] = input(f"Enter new quantity for {item_name}: ")
            print(f"{item_name} updated successfully.")
            return
    print(f"{item_name} not found in inventory.")

def delete_food(inventory):
    display_inventory(inventory)
    item_name = input("Enter the item name to delete: ")
    for item in inventory:
        if item[0] == item_name:
            inventory.remove(item)
            print(f"{item_name} deleted successfully.")
            return
    print(f"{item_name} not found in inventory.")

if __name__ == "__main__":
    main()
