import repo_api as repo
import logging
import logging
from pathlib import Path

LOGS_DIR = Path(__file__).parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / 'client.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.basicConfig(level=logging.INFO)

def menu():
    print("""
    Product Management Menu:
    1 - Add Product
    2 - List Products
    3 - Get by ID
    4 - Update Product
    5 - Delete Product
    6 - Show Total Stock
    7 - Scrape Products
    8 - Exit
    """)
    choice = int(input("Enter choice: "))
    return choice

def run():
    choice = menu()
    while choice != 8:
        try:
            if choice == 1:
                name = input("Name: ")
                qty = int(input("Quantity: "))
                price = float(input("Price: "))
                p = repo.create_product({"name": name, "qty": qty, "price": price})
                print("Added:", p)
            elif choice == 2:
                prods = repo.read_all()
                for p in prods:
                    print(p)
            elif choice == 3:
                pid = int(input("ID: "))
                print(repo.read_by_id(pid))
            elif choice == 4:
                pid = int(input("ID: "))
                name = input("Name: ")
                qty = int(input("Quantity: "))
                price = float(input("Price: "))
                print(repo.update({"id": pid, "name": name, "qty": qty, "price": price}))
            elif choice == 5:
                pid = int(input("ID: "))
                print(repo.delete_by_id(pid))
            elif choice == 6:
                print(repo.get_total_stock())
            elif choice == 7:
                print(repo.scrape_products())
        except Exception as e:
            logging.error(f"Error: {e}")
        choice = menu()

if __name__ == "__main__":
    run()