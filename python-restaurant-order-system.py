from abc import ABC, abstractmethod
import sys

appetizers = []
main_courses = []
desserts = []
beverages = []
orders = []
tables = []
order_id = 0
table_id = 0
active_order_id = -1


class MenuItem(ABC):
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_info(self):
        return f"{self._name}: ${self._price}"

    def get_price(self):
        return self._price

    def get_name(self):
        return self._name


class Appetizer(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)


class MainCourse(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)


class Dessert(MenuItem):
    def __init__(self, name, price):
        super().__init__(name, price)


class Beverage(MenuItem):
    def __init__(self, name, price, is_hot):
        super().__init__(name, price)
        self._is_hot = is_hot


class Order:
    def __init__(self):
        global order_id
        order_id += 1
        self._items = []
        self._order_id = order_id
        self._table_id = table_id
        self._is_active = True

    def add_item(self, item):
        self._items.append(item)

    def show_order(self):
        print(f"Order id: {self._order_id} \nTable id: {self._table_id}")
        for item in self._items:
            print(item.get_info())

    def set_active_order(self, order_id, items):
        self._order_id = order_id
        self._items = items

    def get_total(self):
        total = 0
        for item in self._items:
            total += item.get_price()
        return round(total, 2)

    @property
    def order_id(self):
        return self._order_id

    @property
    def is_active(self):
        return self._is_active

    @property
    def table_id(self):
        return self._table_id

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @table_id.setter
    def table_id(self, value):
        self._table_id = value


class Table():
    def __init__(self):
        global table_id
        table_id += 1
        self._items = []
        self._table_id = table_id
        self._orders = orders
        self._is_available = True

    def show_orders(self):
        print(f"Orders for table id {self._table_id}: {self._order_id}")
        for order in self._orders:
            print(order.show_order())

    @property
    def table_id(self):
        return self._table_id

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, value):
        self._is_available = value


def init_appetizers():
    appetizers.append(Appetizer("Garlic bread", 9.99))
    appetizers.append(Appetizer("Olives", 7.99))


def init_main_courses():
    main_courses.append(MainCourse("Pasta Carbonara", 19.99))
    main_courses.append(MainCourse("Fish and Chips", 27.99))


def init_desserts():
    desserts.append(Dessert("Creme brulee", 12.99))
    desserts.append(Dessert("Ice Cream", 8.99))


def init_beverages():
    beverages.append(Beverage("Water", 0.99, False))
    beverages.append(Beverage("Coffee", 4.99, True))
    beverages.append(Beverage("Lemonade", 1.99, True))


def init_tables():
    tables.append(Table())
    tables.append(Table())


init_appetizers()
init_main_courses()
init_desserts()
init_beverages()
init_tables()


def create_new_order():
    global orders
    global active_order_id
    order = Order()
    active_order_id = order.order_id
    orders.append(order)


def find_order_by_id(order_id):
    global orders
    found = False
    for order in orders:
        if order.order_id == order_id:
            index = orders.index(order)
            found = True
    if found:
        return index
    else:
        return -1


def find_table_by_id(table_id):
    global tables
    found = False
    for table in tables:
        if table.table_id == table_id:
            index = tables.index(table)
            found = True
    if found:
        return index
    else:
        return -1


def assign_table_to_order(table_id):
    global active_order_id
    order = orders[find_order_by_id(active_order_id)]
    order.table_id = table_id
    tables[find_table_by_id(table_id)].is_available = False


def view_order():
    global orders
    print("Please enter order id: ")
    choice = input()
    index = find_order_by_id(int(choice))
    if index != -1:
        orders[index].show_order()
        print(f"Total: ${orders[index].get_total()}")
        print(f"Active order: {orders[index]._is_active}")
    else:
        print("Order not found")


def update_order():
    global orders
    print("Please enter order id: ")
    choice = input()
    index = find_order_by_id(int(choice))
    if orders[index].is_active == False:
        print("Order closed, cannot be updated.")
        return
    if index != -1:
        active_order_id = orders[index].order_id
        orders[index].show_order()
        print(f"Total: ${orders[index].get_total()}")
        print(active_order_id)
        menu_full()
    else:
        print("Order not found")


def close_order():
    global orders
    print("Please enter order id: ")
    choice = input()
    order_index = find_order_by_id(int(choice))
    table_index = find_table_by_id(orders[order_index].table_id)
    if order_index != -1:
        active_order_id = orders[order_index].order_id
        orders[order_index].show_order()
        print(f"Total: ${orders[order_index].get_total()}")
        print(active_order_id)
        tables[table_index].is_available = True
        orders[order_index].is_active = False
    else:
        print("Order not found")


def print_menu(title, category, category_singular):
    while True:
        print(f"{title.title()}")
        i = 0
        for category_singular in category:
            i += 1
            print(f"{i}.  {category_singular.get_info()}")
        print("0. Go back")
        choice = input()
        if choice == "0":
            break
        elif choice.isdigit() and int(choice) <= len(category):
            menu_confirmation(category[int(choice) - 1])
        else:
            print("Invalid choice. Please enter a valid menu item.")


def menu_confirmation(item):
    while True:
        print(f"Would you like to add {item.get_name()} to your order? (y/n)")
        yesorno = input()
        match yesorno:
            case "y":
                orders[find_order_by_id(active_order_id)].add_item(item)
                return
            case "n":
                return
            case _:
                print("Invalid choice. Please choose y(es) or n(o).")


def menu_main():
    while True:
        print("Main menu")
        print("1. Place new order")
        print("2. View order")
        print("3. Update order")
        print("4. Close order")
        print("0. Quit")
        choice = input()
        match choice:
            case "1":
                create_new_order()
                menu_tables()
                menu_full()
            case "2":
                view_order()
            case "3":
                update_order()
            case "4":
                close_order()
            case "0":
                sys.exit()
            case _:
                print("invalid choice. Please enter a valid menu item.")


def menu_tables():
    while True:
        available_tables = []
        shown_tables = {}
        for table in tables:
            if table.is_available:
                available_tables.append(table)
        print("Available tables")
        if len(available_tables) == 0:
            print("There are no available tables.")
        else:
            i = 0
            for table in available_tables:
                i += 1
                print(f"{i}.  Table {table.table_id}")
                shown_tables.setdefault(i, table.table_id)
        print("0. Go back")
        print(shown_tables)
        choice = input()
        if choice == "0":
            menu_main()
        elif choice.isdigit() and int(choice) <= len(available_tables):
            assign_table_to_order(shown_tables.get(int(choice)))
            break
        else:
            print("Invalid choice. Please enter a valid menu item.")


def menu_full():
    while True:
        print("Menu")
        print("1. Appetizers")
        print("2. Main courses")
        print("3. Desserts")
        print("4. Beverages")
        print("0. Go back")
        choice = input()
        match choice:
            case "1":
                menu_appetizers()
            case "2":
                menu_main_courses()
            case "3":
                menu_desserts()
            case "4":
                menu_beverages()
            case "0":
                break
            case _:
                print("Invalid choice. Please enter a valid menu item.")


def menu_appetizers():
    print_menu("Appetizers", appetizers, Appetizer)


def menu_main_courses():
    print_menu("Main Courses", main_courses, MainCourse)


def menu_desserts():
    print_menu("Desserts", desserts, Dessert)


def menu_beverages():
    print_menu("Beverages", beverages, Beverage)


while True:
    menu_main()
