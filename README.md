# Kiosk Manager

Kiosk Manager is a command-line inventory and sales tool designed for small kiosks or shops and written in pure Python. This project was developed as a capstone project focusing on fundamental programming concepts such as functions, dictionaries, lists, tuples, sets, and file I/O.

## Features

- **View Stock**: Display an overview of each product along with its price and quantity in a formatted table.
- **Add/Restock Products**: Add new products or replenish existing stock.
- **Sell Products**: Facilitate sales while verifying stock availability to ensure no more items are sold than are in stock.
- **Sales Report**: Generate a report that includes total revenue, unique products sold, and the top-selling product of the day.
- **Search Products**: Locate products using a partial, case-insensitive name match.
- **Persistent Storage**: Maintain inventory and sales history by saving them to text files, allowing data to carry over between sessions.

## Example Session

```
What is the name of the kiosk: Mama Njeri
What is the name of the owner: Njeri

Welcome to Mama Njeri's Kiosk Manager, run by Njeri.
No save file found. Starting with default inventory.

===== MAIN MENU =====
1. View Stock
2. Add/Restock a Product
3. Sell a Product
4. View Sales Report
5. Search Products
6. Exit

Enter your choice: 1

Product      Price (KES)   Quantity
----------------------------------------
Bread        65            20
Milk         120           15
Eggs         450           8

Enter your choice: 3
Enter product name to sell: bread
How many Bread would you like to sell? 3
Sold 3 Bread for KES 195. Remaining stock: 17

Enter your choice: 4

Product      Qty    Total (KES)
-------------------------------------
Bread        3      195
-------------------------------------
Total revenue: KES 195
Unique products sold today: 1
Best-selling product: Bread (3 units)

Enter your choice: 6
Saving data... Goodbye!
```

## Data Files

- `inventory.txt`: This file contains the current stock and is created automatically upon exit and reloaded during the next session.
- `sales_history.txt`: A running log of sales that is appended to across multiple sessions (the file is never overwritten).

If `inventory.txt` does not exist, the application starts with a small default stock consisting of Bread, Milk, and Eggs so that users can try it immediately.

## Project Structure

```
kiosk_manager.py  # the entire application
```

## Design Notes

This project performs `.isdigit()` checks before any `int()` conversion. Each input that has the potential for errors (such as menu choices, quantities, and prices) is validated before use, ensuring that invalid inputs result in a clear error message instead of causing the program to crash.
