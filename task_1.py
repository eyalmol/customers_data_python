from pathlib import Path
import json
import shutil

from utils import read_orders

def orders_to_customers(data_path: Path, overwrite: bool=True):

    orders_path = Path(f"{data_path.resolve()}/Orders/")
    customers_path = Path(f"{data_path.resolve()}/Customers/")
    
    # Retuen false if customers folders already exsists
    if not overwrite and customers_path.is_dir():
        return False

    # Remove customers path is exists
    if customers_path.is_dir():
        shutil.rmtree(customers_path)

    # Create customers folder
    customers_path.mkdir()

    # Raise exception if no orders dir
    if not orders_path.is_dir():
        raise Exception("Orders dir not exists")

    # Read orders
    orders = read_orders(orders_path)
    
    # Convert orders list into customers list
    customers = {}

    for o in orders:

        customer = o["customer"]
        order = o["order"]
        customer_id = customer["customerID"]
        order_id = order["orderId"]

        if not customer_id in customers:
            customers[customer_id] = {}

        product_max_price = max(p["price"] for p in order["products"])
        products_with_max_price = \
            [p for p in order["products"] if p["price"] == product_max_price]

        customers[customer_id][order_id] = {
            "CustomerFirstName": customer["firstName"],
            "CustomerLastName": customer["lastName"],
            "OrderDate": f"{order['orderMonth']:02}-{str(order['orderYear'])[-2:]}",
            "NumberOfProducts": len(order["products"]),
            "TotalPrice": round(sum(p["price"] for p in order["products"]), 1),
            "ProductWithMaxPrice": products_with_max_price[0]["name"],
            "IsYellowProductIncluded": any("yellow" in p["tags"] for p in order["products"]),
        }
    
    # Create customers folders
    for customer_id, customer in customers.items():
        for order_id, order in customer.items():
            order_path = Path(f"{customers_path.resolve()}/{customer_id}/{order_id}")
            order_path.mkdir(parents=True)
            with open(f"{order_path.resolve()}/OrderSummery.json", "w") as f:
                json.dump(order, f, indent="    ")
    
    return True

