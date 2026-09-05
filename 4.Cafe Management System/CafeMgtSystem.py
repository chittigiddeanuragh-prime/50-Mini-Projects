# Cafe Management System

menu = {
    "Coffee": 50,
    "Tea": 30,
    "Sandwich": 80,
    "Burger": 120,
    "Pizza": 150,
    "French Fries": 90,
    "Cake": 70,
    "Juice": 60
}

order = {}


def display_menu():
    print("\n" + "=" * 40)
    print("             CAFE MENU")
    print("=" * 40)

    for item, price in menu.items():
        print(f"{item:<20} ₹{price}")

    print("=" * 40)


def add_item():
    display_menu()

    item = input("\nEnter item name: ").strip().title()

    if item not in menu:
        print("❌ Item not found in the menu.")
        return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return

    except ValueError:
        print("❌ Please enter a valid number.")
        return

    if item in order:
        order[item] += quantity
    else:
        order[item] = quantity

    print(f"✅ {quantity} x {item} added to your order.")


def view_order():
    if not order:
        print("\n🛒 Your order is empty.")
        return

    print("\n" + "=" * 50)
    print("                 YOUR ORDER")
    print("=" * 50)

    total = 0

    for item, quantity in order.items():
        price = menu[item]
        item_total = price * quantity
        total += item_total

        print(
            f"{item:<20} "
            f"{quantity:<5} "
            f"₹{item_total}"
        )

    print("=" * 50)
    print(f"{'Total':<25} ₹{total}")
    print("=" * 50)


def remove_item():
    if not order:
        print("\n🛒 Your order is empty.")
        return

    view_order()

    item = input("\nEnter item to remove: ").strip().title()

    if item not in order:
        print("❌ That item is not in your order.")
        return

    try:
        quantity = int(input("Enter quantity to remove: "))

        if quantity <= 0:
            print("❌ Quantity must be greater than 0.")
            return

    except ValueError:
        print("❌ Please enter a valid number.")
        return

    if quantity >= order[item]:
        del order[item]
        print(f"✅ {item} removed from your order.")
    else:
        order[item] -= quantity
        print(f"✅ {quantity} x {item} removed.")


def generate_bill():
    if not order:
        print("\n🛒 Your order is empty.")
        return

    print("\n")
    print("=" * 50)
    print("                 CAFE BILL")
    print("=" * 50)

    total = 0

    for item, quantity in order.items():
        price = menu[item]
        item_total = price * quantity
        total += item_total

        print(
            f"{item:<20}"
            f"{quantity:<5}"
            f"₹{item_total}"
        )

    print("-" * 50)

    # GST calculation
    gst = total * 0.05
    grand_total = total + gst

    print(f"{'Subtotal':<30} ₹{total:.2f}")
    print(f"{'GST (5%)':<30} ₹{gst:.2f}")
    print(f"{'Grand Total':<30} ₹{grand_total:.2f}")

    print("=" * 50)
    print("       Thank you for visiting!")
    print("=" * 50)

    order.clear()


def main():
    while True:
        print("\n" + "=" * 40)
        print("       WELCOME TO PYTHON CAFE")
        print("=" * 40)

        print("1. View Menu")
        print("2. Add Item")
        print("3. View Order")
        print("4. Remove Item")
        print("5. Generate Bill")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            display_menu()

        elif choice == "2":
            add_item()

        elif choice == "3":
            view_order()

        elif choice == "4":
            remove_item()

        elif choice == "5":
            generate_bill()

        elif choice == "6":
            print("\n☕ Thank you for using Python Cafe!")
            break

        else:
            print("❌ Invalid choice. Please select 1-6.")


main()