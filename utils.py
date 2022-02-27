from pathlib import Path
import json

def read_orders(orders_path:Path) -> dict:

    orders = []

    for p in orders_path.iterdir():
        if p.is_dir():
            order_path = Path(f"{p.resolve()}/Order.json")
            customer_path = Path(f"{p.resolve()}/Customer.json")
            if order_path.is_file() and customer_path.is_file():
                with order_path.open() as order_file, customer_path.open() as customer_file:
                    order = json.load(order_file)
                    customer = json.load(customer_file)
                orders.append({"order": order, "customer": customer})

    return orders

