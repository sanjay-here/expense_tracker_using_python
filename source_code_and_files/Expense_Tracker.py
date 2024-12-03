from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
import json
import os

# File where data will be stored
DATA_FILE = "expenses.json"

# Load data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to validate inputs
def validateInputs():
    try:
        float(item_amt.get())  # Check if price can be converted to float
        if not item_name.get():
            raise ValueError("Item name cannot be empty.")
        if not transaction_date.get():
            raise ValueError("Transaction date cannot be empty.")
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
        return False
    return True

# Function to save a record
def saveRecord():
    if not validateInputs():
        return  # Do not proceed if inputs are invalid

    global count
    item_name_val = item_name.get()
    item_price_val = float(item_amt.get())
    purchase_date_val = transaction_date.get()

    record = {
        "serial": count,
        "item_name": item_name_val,
        "item_price": item_price_val,
        "purchase_date": purchase_date_val
    }

    # Load the existing data
    data = load_data()
    data.append(record)
    save_data(data)

    # Insert into Treeview
    tv.insert("", "end", iid=count, values=(count, item_name_val, item_price_val, purchase_date_val))
    count += 1

    clearEntries()  # Clear the input fields

# Function to update a selected record
def updateRecord():
    selected = tv.selection()[0]
    item_name_val = item_name.get()
    item_price_val = float(item_amt.get())
    purchase_date_val = transaction_date.get()

    rid = int(tv.item(selected)["values"][0])  # Get row ID

    # Load the existing data
    data = load_data()
    for record in data:
        if record["serial"] == rid:
            record["item_name"] = item_name_val
            record["item_price"] = item_price_val
            record["purchase_date"] = purchase_date_val
            break
    save_data(data)

    # Updating the Treeview display
    tv.item(selected, values=(rid, item_name_val, item_price_val, purchase_date_val))
    clearEntries()

# Function to delete a selected record
def deleteRecord():
    selected = tv.selection()[0]
    rid = int(tv.item(selected)["values"][0])  # Get row ID

    # Load the existing data
    data = load_data()
    data = [record for record in data if record["serial"] != rid]  # Remove the record with the matching ID
    save_data(data)

    # Remove from Treeview
    tv.delete(selected)

# Function to clear the input fields
def clearEntries():
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)

# Function to display total spent
def totalSpent():
    total = 0
    for record in load_data():
        total += record["item_price"]  # Summing up the item prices
    messagebox.showinfo("Overall Expenses", f"Total Expense: Rs. {total}")

# Function to display total balance
def totalBalance():
    total_spent = 0
    try:
        budget = float(budget_entry.get())  # Get the dynamic budget from entry
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the budget.")
        return

    for record in load_data():
        total_spent += record["item_price"]

    balance = budget - total_spent
    messagebox.showinfo("Current Balance", f"Total Expense: Rs. {total_spent}\nBalance Remaining: Rs. {balance}")

# Function to set the current date (if required)
def setDate():
    from datetime import date
    transaction_date.delete(0, END)
    transaction_date.insert(0, date.today().strftime("%d %B %Y"))

# Layout of the GUI
root = Tk()
root.title("Expense Tracker 💰")
root.geometry("820x580")  # Increased height for budget entry

# Initialize
count = 1 if not load_data() else max(record["serial"] for record in load_data()) + 1

# Load and display the image using Pillow
image = Image.open("ET.jpg")  # Use Pillow to open the image

# Resize the image to a desired width and height (e.g., 150x150)
image = image.resize((200, 150), Image.LANCZOS)  # Resize image with LANCZOS resampling
img = ImageTk.PhotoImage(image)  # Convert it for Tkinter

img_label = Label(root, image=img)  # Create a label to display the image
img_label.grid(row=2, column=3, padx=0, pady=0)  # Place the label at the top right corner

# Budget Entry - now placed at the top
Label(root, text="SET BUDGET 💸").grid(row=0, column=0, padx=10, pady=5, sticky='w')
budget_entry = Entry(root)
budget_entry.grid(row=0, column=1, padx=10, pady=5)

# Labels and Entries for expenses
Label(root, text="ITEM NAME 🧾").grid(row=1, column=0, padx=5, pady=5, sticky='w')  # Adjusted padx
item_name = Entry(root)
item_name.grid(row=1, column=1, padx=10, pady=5)  # Adjusted padx

Label(root, text="ITEM PRICE 💲").grid(row=2, column=0, padx=5, pady=5, sticky='w')  # Adjusted padx
item_amt = Entry(root)
item_amt.grid(row=2, column=1, padx=10, pady=5)  # Adjusted padx

Label(root, text="PURCHASE DATE 📅").grid(row=3, column=0, padx=5, pady=5, sticky='w')  # Adjusted padx
transaction_date = Entry(root)
transaction_date.grid(row=3, column=1, padx=10, pady=5)  # Adjusted padx

# Uniform Padding for Buttons
button_padx = 5

# Buttons for Save, Update, Clear Entry, Delete, Current Date, and Exit
Button(root, text="Save Record", command=saveRecord, bg="green", fg="white").grid(row=4, column=1, padx=button_padx, pady=5)
Button(root, text="Update", command=updateRecord, bg="yellow").grid(row=4, column=2, padx=button_padx, pady=5)
Button(root, text="Delete", command=deleteRecord, bg="red", fg="white").grid(row=4, column=3, padx=button_padx, pady=5)
Button(root, text="Current Date", command=setDate).grid(row=4, column=4, padx=button_padx, pady=5)  
Button(root, text="Clear Entry", command=clearEntries).grid(row=4, column=5, padx=button_padx, pady=5)
Button(root, text="Exit", command=root.quit).grid(row=4, column=6, padx=button_padx, pady=5)

# Buttons for Total Spent and Total Balance
Button(root, text="Total Spent", command=totalSpent).grid(row=6, column=2, padx=button_padx, pady=5)
Button(root, text="Total Balance", command=totalBalance).grid(row=6, column=3, padx=button_padx, pady=5)

# Treeview to display records
columns = ('serial', 'item_name', 'item_price', 'purchase_date')
tv = ttk.Treeview(root, columns=columns, show='headings')

tv.heading('serial', text="Serial no")
tv.heading('item_name', text="Item Name")
tv.heading('item_price', text="Item Price")
tv.heading('purchase_date', text="Purchase Date")

tv.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

# Load existing records into the Treeview
for record in load_data():
    tv.insert("", "end", iid=record["serial"], values=(record["serial"], record["item_name"], record["item_price"], record["purchase_date"]))

root.mainloop()
