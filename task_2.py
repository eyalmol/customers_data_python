from pathlib import Path
from statistics import mean
import csv

from utils import read_orders

def create_customers_csv(data_path: Path, overwrite: bool=True):

    orders_path = Path(f"{data_path.resolve()}/Orders/")
    customers_csv_path = Path(f"{data_path.resolve()}/Customers.csv")
    
    # Retuen false if customers csv already exsists
    if not overwrite and customers_csv_path.is_file():
        return False

    # Raise exception if no orders dir
    if not orders_path.is_dir():
        raise Exception("Orders dir not exists")

    # Read orders
    orders = read_orders(orders_path)

    # Convert orders list into customers list with orders prices
    customers_orders_prices = {}

    for o in orders:

        customer = o["customer"]
        order = o["order"]
        customer_id = customer["customerID"]

        if not customer_id in customers_orders_prices:
            customers_orders_prices[customer_id] = []

        customers_orders_prices[customer_id].append(
            sum(p["price"] for p in order["products"])
        )

    with open(customers_csv_path, "w", newline='') as f:
        csv_writer = csv.writer(f)

        # Write header
        csv_writer.writerow([
            "CustomerID",
            "NumberOfOrders",
            "TotalPriceOfAllOrders",
            "AvgPriceOfOrders",
        ])

        # Write customers
        for customer_id, customer_orders_prices in customers_orders_prices.items():
            csv_writer.writerow([
                customer_id,
                len(customer_orders_prices),
                round(sum(customer_orders_prices), 1),
                round(mean(customer_orders_prices), 1),
            ])
    
    return True