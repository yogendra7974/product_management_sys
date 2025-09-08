import sqlite3
import logging
from utils import setup_logger

DB_PATH = 'product_db.sqlite'

logger = setup_logger(__name__)
logger.info("Creating product table if not exists...")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def connect():
    return sqlite3.connect(DB_PATH)


def product_table_create():
    sql = """
    CREATE TABLE IF NOT EXISTS product(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        qty INTEGER NOT NULL,
        price REAL NOT NULL
    );
    """
    try:
        con = connect()
        con.execute(sql)
        con.close()
        logging.info("Product table ready.")
    except Exception as e:
        logging.error(f"DB init error: {e}")


class Product:
    def __init__(self, id=None, name='', qty=0, price=0.0):
        self.id = id
        self.name = name
        self.qty = qty
        self.price = price


def create_product(product):
    sql = "INSERT INTO product(name, qty, price) VALUES (?, ?, ?)"
    try:
        con = connect()
        cur = con.cursor()
        cur.execute(sql, (product.name, product.qty, product.price))
        product_id = cur.lastrowid
        con.commit()
        con.close()
        return product_id
    except Exception as e:
        logging.error(f"Create product failed: {e}")
        raise


def read_all_products():
    sql = "SELECT id, name, qty, price FROM product"
    con = connect()
    cur = con.cursor()
    result = cur.execute(sql).fetchall()
    con.close()
    return [Product(id=row[0], name=row[1], qty=row[2], price=row[3]) for row in result]


def read_product_by_id(prod_id):
    sql = "SELECT id, name, qty, price FROM product WHERE id=?"
    con = connect()
    cur = con.cursor()
    row = cur.execute(sql, (prod_id,)).fetchone()
    con.close()
    if row:
        return Product(id=row[0], name=row[1], qty=row[2], price=row[3])
    return None


def update_product(product):
    sql = "UPDATE product SET name=?, qty=?, price=? WHERE id=?"
    con = connect()
    cur = con.cursor()
    cur.execute(sql, (product.name, product.qty, product.price, product.id))
    con.commit()
    con.close()


def delete_product(prod_id):
    sql = "DELETE FROM product WHERE id=?"
    con = connect()
    cur = con.cursor()
    cur.execute(sql, (prod_id,))
    con.commit()
    con.close()