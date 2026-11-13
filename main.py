
import logging
from abc import ABC, abstractmethod



logging.basicConfig(
    filename="application.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


class ProductNotFoundError(Exception):
    pass


class DuplicateProductError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InvalidProductDataError(Exception):
    pass


class Product(ABC):

    total_products = 0

    def __init__(self, product_id, name, price, quantity):
        if not self.valid_id(product_id):
            raise InvalidProductDataError("Invalid product ID.")

        if name.strip() == "":
            raise InvalidProductDataError("Product name cannot be empty.")

        if price < 0:
            raise InvalidProductDataError("Price cannot be negative.")

        if quantity < 0:
            raise InvalidProductDataError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.__price = price
        self.__quantity = quantity

        Product.total_products += 1

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price < 0:
            raise InvalidProductDataError("Price cannot be negative.")

        self.__price = price

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise InvalidProductDataError("Quantity cannot be negative.")

        self.__quantity = quantity

    def update_stock(self, quantity):
        if quantity < 0:
            raise InvalidProductDataError("Stock cannot be negative.")

        self.__quantity = quantity

    def display_details(self):
        print("Product ID:", self.product_id)
        print("Product Name:", self.name)
        print("Category:", self.__class__.__name__)
        print("Price:", self.__price)
        print("Quantity:", self.__quantity)

    @abstractmethod
    def calculate_discount(self):
        pass

    @classmethod
    def show_product_count(cls):
        print("Total Products:", cls.total_products)

    @staticmethod
    def valid_id(product_id):
        return product_id.strip() != ""

    def __str__(self):
        return self.product_id + " " + self.name

    def __del__(self):
        pass


class GroceryProduct(Product):

    def __init__(self, product_id, name, price, quantity):
        super().__init__(product_id, name, price, quantity)

    def calculate_discount(self):
        return self.get_price() * 0.05


class ElectronicsProduct(Product):

    def __init__(self, product_id, name, price, quantity):
        super().__init__(product_id, name, price, quantity)

    def calculate_discount(self):
        return self.get_price() * 0.10


class ClothingProduct(Product):

    def __init__(self, product_id, name, price, quantity):
        super().__init__(product_id, name, price, quantity)

    def calculate_discount(self):
        return self.get_price() * 0.15


class InventoryManager:

    def __init__(self):
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            raise DuplicateProductError("Duplicate product ID.")

        self.products[product.product_id] = product
        logging.info("Product added: %s", product.product_id)

    def view_products(self):
        if len(self.products) == 0:
            print("Inventory is empty.")
            return

        for product in self.products.values():
            product.display_details()
            print("--------------------")

        Product.show_product_count()

    def search_product(self, product_id):
        if product_id not in self.products:
            raise ProductNotFoundError("Product not found.")

        return self.products[product_id]

    def update_product(self, product_id, price, quantity):
        product = self.search_product(product_id)

        product.set_price(price)
        product.update_stock(quantity)

        print("Product updated successfully.")
        logging.info("Product updated: %s", product_id)

    def remove_product(self, product_id):
        product = self.search_product(product_id)

        del self.products[product_id]
        Product.total_products -= 1

        print("Product removed successfully.")
        logging.info("Product removed: %s", product_id)

    def check_stock(self, product_id, quantity):
        product = self.search_product(product_id)

        if quantity > product.get_quantity():
            raise InsufficientStockError("Not enough stock available.")

    def reduce_stock(self, product_id, quantity):
        product = self.search_product(product_id)

        new_quantity = product.get_quantity() - quantity
        product.update_stock(new_quantity)

        logging.info("Stock updated: %s", product_id)


class Customer:

    def __init__(self, name, phone):
        if name.strip() == "":
            raise InvalidProductDataError("Customer name cannot be empty.")

        self.name = name
        self.phone = phone

    def display_details(self):
        print("Customer Name:", self.name)
        print("Phone:", self.phone)



class Order:

    order_count = 0

    def __init__(self, customer):
        Order.order_count += 1

        self.order_id = "ORD" + str(Order.order_count)
        self.customer = customer
        self.items = []

    def add_item(self, product, quantity=1):
        if quantity <= 0:
            raise InvalidProductDataError(
                "Order quantity must be greater than zero."
            )

        if quantity > product.get_quantity():
            raise InsufficientStockError("Not enough stock available.")

        self.items.append((product, quantity))

    def calculate_total(self):
        total = 0

        for product, quantity in self.items:
            price = product.get_price()
            discount = product.calculate_discount()

            item_total = (price - discount) * quantity
            total += item_total

        return total

    def generate_bill(self):
        print("\n========== BILL ==========")
        print("Order ID:", self.order_id)
        self.customer.display_details()

        grand_total = 0

        print("\nProduct Details")

        for product, quantity in self.items:
            price = product.get_price()
            discount = product.calculate_discount()

            item_total = price * quantity
            discount_total = discount * quantity
            final_amount = item_total - discount_total

            print("\nProduct:", product.name)
            print("Quantity:", quantity)
            print("Unit Price:", price)
            print("Discount:", round(discount_total, 2))
            print("Item Total:", round(final_amount, 2))

            grand_total += final_amount

        print("--------------------------")
        print("Grand Total:", round(grand_total, 2))
        print("==========================")

    def __len__(self):
        return len(self.items)

def get_number(message, number_type=float):

    while True:
        try:
            value = number_type(input(message))

        except ValueError:
            print("Please enter a valid number.")
            logging.warning("Invalid numeric input")

        else:
            return value

        finally:
            print("Input completed.")



def add_product_menu(inventory):

    print("\n1. Grocery  2. Electronics  3. Clothing")

    category = input("Choose category: ")

    product_id = input("Product ID: ")
    name = input("Product name: ")
    price = get_number("Price: ", float)
    quantity = get_number("Quantity: ", int)

    if category == "1":
        product = GroceryProduct(product_id, name, price, quantity)

    elif category == "2":
        product = ElectronicsProduct(product_id, name, price, quantity)

    elif category == "3":
        product = ClothingProduct(product_id, name, price, quantity)

    else:
        raise InvalidProductDataError("Invalid category.")

    inventory.add_product(product)

    print("Product added successfully.")



def place_order_menu(inventory, orders):

    name = input("Customer name: ")
    phone = input("Customer phone: ")

    customer = Customer(name, phone)
    order = Order(customer)

    while True:

        product_id = input("Enter Product ID: ")
        quantity = get_number("Enter quantity: ", int)

        product = inventory.search_product(product_id)

        inventory.check_stock(product_id, quantity)
        order.add_item(product, quantity)

        choice = input("Add another product? (yes/no): ").lower()

        if choice != "yes":
            break

    if len(order) == 0:
        print("No products added to the order.")
        return

    
    for product, quantity in order.items:
        inventory.reduce_stock(product.product_id, quantity)

    orders.append(order)

    order.generate_bill()

    logging.info("Order completed: %s", order.order_id)



def main():

    inventory = InventoryManager()
    orders = []

    while True:

        print("\n===== INVENTORY AND ORDER MANAGEMENT =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Remove Product")
        print("6. Place Order")
        print("7. View Orders")
        print("8. Exit")

        choice = input("Enter choice: ")

        try:

            if choice == "1":
                add_product_menu(inventory)

            elif choice == "2":
                inventory.view_products()

            elif choice == "3":
                product_id = input("Enter Product ID: ")

                product = inventory.search_product(product_id)
                product.display_details()

            elif choice == "4":
                product_id = input("Enter Product ID: ")

                price = get_number("Enter new price: ", float)
                quantity = get_number("Enter new quantity: ", int)

                inventory.update_product(product_id, price, quantity)

            elif choice == "5":
                product_id = input("Enter Product ID: ")

                inventory.remove_product(product_id)

            elif choice == "6":
                place_order_menu(inventory, orders)

            elif choice == "7":

                if len(orders) == 0:
                    print("No orders available.")

                else:
                    for order in orders:
                        order.generate_bill()

            elif choice == "8":
                print("Thank you for using the system.")
                break

            else:
                print("Invalid menu choice.")
                logging.warning("Invalid menu choice: %s", choice)

        except DuplicateProductError as e:
            print(e)
            logging.warning("Duplicate product attempt")

        except ProductNotFoundError as e:
            print(e)
            logging.warning("Product not found")

        except InsufficientStockError as e:
            print(e)
            logging.warning("Order rejected due to insufficient stock")

        except InvalidProductDataError as e:
            print(e)
            logging.warning("Invalid product or customer data")

        except ValueError as e:
            print("Invalid input:", e)
            logging.warning("Invalid value entered")

        except (KeyboardInterrupt, EOFError):
            print("\nProgram stopped by user.")
            logging.warning("Program interrupted")
            break

        except Exception:
            print("An unexpected error occurred.")
            logging.exception("Unexpected error")

        else:
            logging.debug("Menu operation completed")

        finally:
            print("Returning to menu.")


if __name__ == "__main__":
    main()
