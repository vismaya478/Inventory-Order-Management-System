# Inventory & Order Management System

## Project Description

The Inventory & Order Management System is a Python-based application used to manage products, maintain stock details, and handle customer orders.

The system allows users to add, view, search, update, and remove products. It also allows customers to place orders, calculates discounts, and generates itemised bills.

## Features

- Add new products with product ID, name, price, quantity, and category.
- View all available products and their stock details.
- Search for products using their ID.
- Update product price and quantity.
- Remove products from the inventory.
- Place customer orders by selecting products and quantities.
- Check stock availability before confirming an order.
- Calculate item totals and category-based discounts.
- Generate an itemised bill with the grand total.
- View orders placed during the current program execution.
- Record application activities and errors in a log file.

## Technologies Used

- Python
- Object-Oriented Programming
- Python Logging Module

## OOP Concepts Used

### 1. Classes and Objects
Classes such as `Product`, `Customer`, `Order`, and `InventoryManager` are used to organise the program. Objects are created from these classes to manage products and orders.

### 2. Inheritance
`GroceryProduct`, `ElectronicsProduct`, and `ClothingProduct` inherit from the `Product` class.

### 3. Encapsulation
Private attributes are used for product price and quantity. Getter and setter methods are used to access and update these values.

### 4. Abstraction
The `Product` class uses the `ABC` module and an abstract method called `calculate_discount()`.

### 5. Polymorphism
Different product categories have their own implementation of the `calculate_discount()` method.

### 6. Class Methods and Static Methods
A class method is used to display the total number of products. A static method is used to validate product IDs.

### 7. Method Overloading
Default arguments are used in methods to allow them to work with different numbers of arguments.

### 8. Magic Methods
`__str__()` is used to return product information as a string, and `__len__()` is used to return the number of items in an order.

## Exception Handling

The program uses exception handling to manage errors and invalid inputs.

- `try` and `except` are used to handle invalid numeric inputs and other errors.
- `else` and `finally` are used in input handling.
- `raise` is used to raise exceptions when invalid data is entered.
- Custom exceptions include:
  - `ProductNotFoundError`
  - `DuplicateProductError`
  - `InsufficientStockError`
  - `InvalidProductDataError`

## Logging

The program uses Python's logging module to record application activities in `application.log`.

The log file records:
- Successful product additions and updates.
- Product removal.
- Stock updates.
- Successful orders.
- Invalid attempts and warnings.
- Debug information.

## Discount Rules

The following discount percentages are used in the project:

| Product Category | Discount |
|---|---:|
| Grocery | 5% |
| Electronics | 10% |
| Clothing | 15% |

## How to Run the Project

1. Make sure Python is installed on your computer.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run the following command:

```bash
python main.py
```

5. Select an option from the menu and follow the instructions.

## Project Files

| File | Description |
|---|---|
| `main.py` | Contains the complete Python source code. |
| `README.md` | Contains project details and instructions. |
| `application.log` | Stores application activity and log messages. |

