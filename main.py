from pathlib import Path
import json

from task_1 import orders_to_customers
from task_2 import create_customers_csv

SETTINGS_PATH = "settings.json"
DATA_PATH = "data/"

def main():

    settings = {}

    # Read settings file
    with Path(SETTINGS_PATH) as settings_file:
        if settings_file.is_file():
            with open(settings_file) as f:
                settings = json.load(f)

    data_path = Path(settings.get("data_path", DATA_PATH))

    orders_to_customers(data_path)
    create_customers_csv(data_path)

if __name__ == '__main__':
    main()