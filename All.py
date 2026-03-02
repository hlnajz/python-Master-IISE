import streamlit as st

# --- YOUR LOGIC FUNCTIONS ---
def add_item(inventory, name, quantity):                
    if quantity <= 0:
        return inventory
    inventory.update({name: inventory.get(name, 0) + quantity})
    return inventory

def remove_item(inventory, name, quantity):
    current = inventory.get(name)
    if current is None or quantity <= 0:
        return inventory
    if current >= quantity:
        inventory.update({name: current - quantity})
    return inventory

def merge_inventories(inventory, new_inventory):
    for name, qty in new_inventory.items():
        inventory.update({name: inventory.get(name, 0) + qty})
    return inventory

def delete_product(inventory, name):
    inventory.pop(name, None)
    return inventory

# --- STREAMLIT UI SETUP ---
st.title("📦 Inventory Management System")

# Initialize inventory in session state so it persists between clicks
if 'inventory' not in st.session_state:
    st.session_state['inventory'] = {"Laptop": 10, "Mouse": 25}

# Display current inventory
st.subheader("Current Inventory")
st.write(st.session_state['inventory'])

# --- INTERACTIVE CONTROLS ---
st.divider()
tab1, tab2, tab3 = st.tabs(["Add/Remove Items", "Merge Inventory", "Delete Product"])

with tab1:
    st.subheader("Add or Remove")
    col1, col2, col3 = st.columns(3)
    item_name = col1.text_input("Item Name")
    item_qty = col2.number_input("Quantity", min_value=1, step=1)
    
    if col3.button("Add Item"):
        st.session_state['inventory'] = add_item(st.session_state['inventory'], item_name, item_qty)
        st.rerun()
    
    if col3.button("Remove Item"):
        st.session_state['inventory'] = remove_item(st.session_state['inventory'], item_name, item_qty)
        st.rerun()

with tab2:
    st.subheader("Merge Bulk Inventory")
    st.write("Enter items as 'Name:Quantity' separated by commas.")
    bulk_input = st.text_input("Input", "Keyboard:5, Monitor:2")
    if st.button("Merge"):
        # Basic parsing
        new_items = {}
        for pair in bulk_input.split(','):
            key, val = pair.split(':')
            new_items[key.strip()] = int(val)
        
        st.session_state['inventory'] = merge_inventories(st.session_state['inventory'], new_items)
        st.rerun()

with tab3:
    st.subheader("Delete Product")
    prod_to_delete = st.text_input("Product Name to Remove Completely")
    if st.button("Delete"):
        st.session_state['inventory'] = delete_product(st.session_state['inventory'], prod_to_delete)
        st.rerun()