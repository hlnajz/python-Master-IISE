def add_item(inventory, name, quantity):
    inventory.setdefault(name, 0)
    inventory[name] += quantity
    return inventory

def remove_item(inventory, name, quantity):
    if inventory.get(name, 0) >= quantity:
        inventory[name] -= quantity
    else:
        print(f"Error: Not enough stock for '{name}'")
    return inventory

def merge_inventories(inventory, new_inventory):
    for name, quantity in new_inventory.items():
        add_item(inventory, name, quantity)
    return inventory

def delete_product(inventory, name):
    inventory.pop(name, None)
    return inventory

if __name__ == "__main__":
    # Initialize inventory
    my_inventory = {"apple": 10, "banana": 5}
    print(f"Initial Inventory: {my_inventory}")

    # 1. Add item
    add_item(my_inventory, "orange", 20)
    add_item(my_inventory, "apple", 5)
    print(f"After adding: {my_inventory}")

    # 2. Remove item
    remove_item(my_inventory, "banana", 3)
    print(f"After removing: {my_inventory}")

    # 3. Merge inventories
    incoming_shipment = {"banana": 10, "kiwi": 15}
    merge_inventories(my_inventory, incoming_shipment)
    print(f"After merging: {my_inventory}")

    # 4. Delete product
    delete_product(my_inventory, "apple")
    print(f"After deleting apple: {my_inventory}")