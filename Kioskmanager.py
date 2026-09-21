##############################################################################
# KIOSK MANAGER - Capstone Project
#
# IMPORTANT: Python reads a file from TOP to BOTTOM. Before Python can CALL
# a function (like view_stock(stock)), it must have already read that
# function's "def" block earlier in the file.
#
# That's why this file is organised like this:
#   1. All our FUNCTIONS are defined first (the "recipes")
#   2. The ACTUAL PROGRAM (welcome message, menu loop) runs at the bottom
#      (this is where we actually "use" the recipes)
#
# We do NOT use try/except anywhere in this file, because this project only
# uses skills from Sessions 1-6, and try/except hasn't been covered yet.
# Instead, every risky input is checked with .isdigit() BEFORE we convert it
# with int() - same trick you already used in the main menu.
##############################################################################

import os  # only used for os.path.exists() - checking if a save file exists

# File names where we save/load data between runs (Step 7)
INVENTORY_FILE = "inventory.txt"
SALES_FILE = "sales_history.txt"


##############################################################################
# STEP 3: INVENTORY MANAGEMENT
# Two functions: one to VIEW stock, one to RESTOCK/ADD a product.
# Neither of these touches the menu loop directly - they just take "stock"
# in as a parameter and work with it.
##############################################################################

def view_stock(stock):
    """Print every product in stock, lined up neatly in columns."""

    # if the dictionary is empty, there's nothing to show
    if not stock:
        print("No products in stock yet.")
        return

    print()
    # {'Product':<15} means: print the word "Product", left-aligned,
    # padded out to take up 15 characters of space.
    # {'Price (KES)':>13} means: right-aligned, padded to 13 characters.
    # Right-aligning numbers makes columns of digits line up neatly.
    print(f"{'Product':<15}{'Price (KES)':>13}{'Quantity':>12}")
    print("-" * 40)

    # .items() lets us loop through a dictionary and get BOTH the key
    # (name) and the value (details) at the same time.
    for name, details in stock.items():
        print(f"{name:<15}{details['price']:>13}{details['quantity']:>12}")
    print()


def restock_product(stock):
    """Add stock to an existing product, or create a brand new product."""

    # .strip() removes accidental spaces the user typed by mistake.
    # .title() makes sure "bread" and "BREAD" both become "Bread",
    # so we don't accidentally create two different entries for the
    # same product just because of capitalisation.
    name = input("Enter product name: ").strip().title()

    # "in" checks if this name already exists as a KEY in the dictionary
    if name in stock:
        # ---- EXISTING PRODUCT: just add more quantity ----
        raw_amount = input(f"How many {name} to add? ").strip()

        # check it's actually a whole number BEFORE converting with int()
        if not raw_amount.isdigit():
            print("That's not a valid whole number. Restock cancelled.")
            return

        amount = int(raw_amount)

        if amount <= 0:
            print("Amount must be greater than zero. Restock cancelled.")
            return

        # update the quantity inside the nested dictionary
        stock[name]['quantity'] += amount
        print(f"Restocked {name}. New quantity: {stock[name]['quantity']}")

    else:
        # ---- BRAND NEW PRODUCT: we need a price too ----
        print(f"'{name}' is a new product.")

        raw_price = input(f"Enter price for {name} (KES): ").strip()
        raw_quantity = input(f"Enter starting quantity for {name}: ").strip()

        # both inputs must be valid whole numbers, or we cancel
        if not raw_price.isdigit() or not raw_quantity.isdigit():
            print("Price and quantity must be whole numbers. Product not added.")
            return

        price = int(raw_price)
        quantity = int(raw_quantity)

        # create a brand new dictionary entry for this product
        stock[name] = {'price': price, 'quantity': quantity}
        print(f"Added new product: {name}")


##############################################################################
# STEP 4: SELLING A PRODUCT
# Checks stock is available BEFORE changing anything. If there isn't enough,
# we print a message and return immediately - nothing gets changed.
##############################################################################

def sell_product(stock, sales_log, sold_today):
   # """Sell a product: check stock, reduce quantity, log the sale."""

    name = input("Enter product name to sell: ").strip().title()

    # if the product doesn't exist in our dictionary at all, stop here
    if name not in stock:
        print(f"'{name}' is not a product we stock.")
        return

    raw_amount = input(f"How many {name} to sell? ").strip()

    # check it's a valid whole number before converting
    if not raw_amount.isdigit():
        print("Please enter a valid whole number for quantity.")
        return

    amount = int(raw_amount)

    if amount <= 0:
        print("Quantity must be greater than zero.")
        return

    # how many do we currently have of this product?
    available = stock[name]['quantity']

    # THE STOCK CHECK: if they want more than we have, refuse the sale
    if amount > available:
        print(f"Not enough stock. Only {available} {name} left.")
        return

    # ---- if we reach this line, the sale is allowed to go ahead ----

    # reduce the stock quantity
    stock[name]['quantity'] -= amount

    # work out how much this sale is worth
    total = stock[name]['price'] * amount

    # record this sale as a TUPLE (item, quantity, total), added to our LIST
    sales_log.append((name, amount, total))

    # add this product's name to the SET of unique products sold today
    # (sets automatically ignore duplicates, so this is safe to call every time)
    sold_today.add(name)

    print(f"Sold {amount} {name} for KES {total}. Remaining stock: {stock[name]['quantity']}")


##############################################################################
# STEP 5: SALES REPORT
# Goes through every sale, adds up revenue, counts unique products sold,
# and works out which product sold the most units.
##############################################################################

def sales_report(sales_log, sold_today):
    """Print every sale, total revenue, unique products sold, and the best-seller."""

    # if no sales have happened yet, there's nothing to report
    if not sales_log:
        print("No sales recorded yet today.")
        return

    print()
    print(f"{'Product':<15}{'Qty':>8}{'Total (KES)':>14}")
    print("-" * 37)

    # ACCUMULATOR: starts at 0, grows a little bit on every loop pass,
    # ends up holding the full total once the loop finishes
    total_revenue = 0

    # this dictionary will track: {'Bread': 5, 'Milk': 2, ...}
    # i.e. how many units of each product were sold today in total
    quantity_by_product = {}

    # sales_log is a LIST of TUPLES, e.g. [('Bread', 2, 130), ('Milk', 1, 120)]
    # this loop "unpacks" each tuple into three variables at once
    for name, qty, total in sales_log:
        print(f"{name:<15}{qty:>8}{total:>14}")

        # add this sale's total onto our running revenue total
        total_revenue += total

        # .get(name, 0) means: "give me the current count for this product,
        # or 0 if we haven't seen it before" - this avoids a crash on the
        # first time we see a new product name
        quantity_by_product[name] = quantity_by_product.get(name, 0) + qty

    print("-" * 37)
    print(f"Total revenue: KES {total_revenue}")

    # the SET from Step 4 already only holds each product name ONCE,
    # no matter how many times it was sold - so len() gives us the
    # count of unique products directly
    print(f"Unique products sold today: {len(sold_today)}")

    # max() normally finds the biggest number in a list.
    # Here we tell it to look through quantity_by_product's KEYS,
    # but compare them using their VALUES (via key=...get), so it
    # hands back whichever product name had the highest quantity sold.
    best_product = max(quantity_by_product, key=quantity_by_product.get)
    best_qty = quantity_by_product[best_product]
    print(f"Best-selling product: {best_product} ({best_qty} units)")
    print()


##############################################################################
# STEP 6: SEARCH PRODUCTS
# Lets the user search using just PART of a product's name.
# Case doesn't matter, because we lower() both sides before comparing.
##############################################################################

def search_products(stock):
    """Find every product whose name contains the search term."""

    # .lower() so the search isn't case-sensitive (e.g. "BRE" still matches "Bread")
    term = input("Enter part of a product name to search: ").strip().lower()

    matches = {}

    for name, details in stock.items():
        # "in" checks whether "term" appears ANYWHERE inside name.lower()
        # e.g. "bre" in "bread" -> True
        if term in name.lower():
            matches[name] = details

    # if nothing matched, say so and stop here
    if not matches:
        print("No matches found.")
        return

    print()
    print(f"{'Product':<15}{'Price (KES)':>13}{'Quantity':>12}")
    print("-" * 40)
    for name, details in matches.items():
        print(f"{name:<15}{details['price']:>13}{details['quantity']:>12}")
    print()


##############################################################################
# STEP 7: SAVING AND LOADING DATA (FILES)
# Three functions:
#   - load_inventory(): runs ONCE at startup
#   - save_inventory(): runs when the user exits, OVERWRITES the file
#   - save_sales_log(): runs when the user exits, ADDS on to the file
##############################################################################

def load_inventory():
    """Load inventory from file if it exists, otherwise start with a default stock."""

    # os.path.exists() just checks "is there a file with this name?"
    # and gives back True or False - it does NOT open or crash on anything.
    if not os.path.exists(INVENTORY_FILE):
        print("No save file found. Starting with default inventory.")
        return {
            'Bread': {'price': 65, 'quantity': 20},
            'Milk': {'price': 120, 'quantity': 15},
            'Eggs': {'price': 450, 'quantity': 8},
        }

    stock = {}

    # "with open(...) as f" opens the file and automatically closes it
    # again once we're done - even if something goes wrong inside.
    with open(INVENTORY_FILE, "r") as f:
        # a file can be looped through line by line
        for line in f:
            line = line.strip()  # remove the invisible newline at the end

            if not line:
                continue  # skip any blank lines

            # a saved line looks like: "Bread,65,20"
            # .split(",") turns that into a list: ["Bread", "65", "20"]
            name, price, quantity = line.split(",")

            # everything read from a text file comes back as TEXT (a string),
            # even "65" - so we must convert price/quantity back to int()
            stock[name] = {'price': int(price), 'quantity': int(quantity)}

    print("Inventory loaded from save file.")
    return stock


def save_inventory(stock):
    """Write the CURRENT inventory to file, replacing whatever was there before."""

    # "w" = write mode. This OVERWRITES the whole file with fresh content,
    # which is correct here because inventory should always show the
    # LATEST state, not old history.
    with open(INVENTORY_FILE, "w") as f:
        for name, details in stock.items():
            f.write(f"{name},{details['price']},{details['quantity']}\n")


def save_sales_log(sales_log):
    """Add this session's sales onto the END of the sales history file."""

    # "a" = append mode. This ADDS new lines to the end of the file without
    # deleting what was already saved from previous sessions.
    with open(SALES_FILE, "a") as f:
        for name, qty, total in sales_log:
            f.write(f"{name},{qty},{total}\n")


##############################################################################
# STEP 1: WELCOME & SETUP
##############################################################################

def welcome():
    """Ask for the kiosk name and owner name, then print a clean welcome banner."""

    kiosk_name = input("What is the name of the kiosk: ").strip().title()
    owner_name = input("What is the name of the owner: ").strip().title()

    print()
    print(f"Welcome to {kiosk_name}'s Kiosk Manager, run by {owner_name}.")


##############################################################################
# THE ACTUAL PROGRAM STARTS HERE
# Everything above this point was just DEFINING functions - none of that
# code has run yet. This is the part that actually executes.
##############################################################################

# ---- STEP 1: show the welcome banner ----
welcome()

# ---- STEP 7: load saved inventory (or start with defaults) ----
stock = load_inventory()

# ---- STEP 4/5: set up empty tracking for this session ----
sales_log = []      # a LIST that will hold TUPLES, e.g. [('Bread', 2, 130), ...]
sold_today = set()  # a SET that will hold unique product names sold today

# ---- STEP 2: the main menu loop ----
while True:
    print()
    print("===== MAIN MENU =====")
    print("1. View Stock")
    print("2. Add/Restock a Product")
    print("3. Sell a Product")
    print("4. View Sales Report")
    print("5. Search Products")
    print("6. Exit")
    print()

    raw_choice = input("Enter your choice: ").strip()

    # check it's a number BEFORE trying to convert it with int() -
    # this is what stops a typo like "banana" from crashing the program
    if not raw_choice.isdigit():
        print("Please enter a number from the menu.")
        continue  # skip straight back to the top of the loop

    choice = int(raw_choice)

    if choice == 1:
        view_stock(stock)
    elif choice == 2:
        restock_product(stock)
    elif choice == 3:
        sell_product(stock, sales_log, sold_today)
    elif choice == 4:
        sales_report(sales_log, sold_today)
    elif choice == 5:
        search_products(stock)
    elif choice == 6:
        # ---- STEP 7: save everything before closing the program ----
        save_inventory(stock)
        save_sales_log(sales_log)
        print("Saving data... Goodbye!")
        break  # this is what actually stops the "while True" loop
    else:
        # choice was a number, but not 1-6 (e.g. they typed "9")
        print("That's not a valid option, please choose 1-6.")