import logging
from concurrent.futures import ThreadPoolExecutor
from product_repo import read_all_products

logging.basicConfig(level=logging.INFO)


def batch_stock_sum(products_batch):
    return sum(p.qty for p in products_batch)


def total_stock():
    products = read_all_products()
    total = 0
    batch_size = 10
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(products), batch_size):
            batch = products[i:i+batch_size]
            futures.append(executor.submit(batch_stock_sum, batch))
        for f in futures:
            total += f.result()
    logging.info(f"Total stock calculated: {total}")
    return total