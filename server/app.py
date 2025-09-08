from flask import Flask, request, jsonify
from datetime import datetime
import logging
from mail_send import send_gmail
import product_repo as repo
import stock_calc
import scraper

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
repo.product_table_create()


@app.route("/products", methods=['GET'])
def get_all():
    products = repo.read_all_products()
    return jsonify([p.__dict__ for p in products])


@app.route("/products/<int:prod_id>", methods=['GET'])
def get_by_id(prod_id):
    product = repo.read_product_by_id(prod_id)
    if not product:
        return jsonify({"error": "Not found"}), 404
    return jsonify(product.__dict__)


@app.route("/products", methods=['POST'])
def create():
    data = request.get_json()
    try:
        prod = repo.Product(name=data['name'], qty=data['qty'], price=data['price'])
        pid = repo.create_product(prod)
        saved = repo.read_product_by_id(pid)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_gmail("owner@example.com", f"Product Created at {now_str}", f"{saved.__dict__}")
        return jsonify(saved.__dict__), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/products/<int:prod_id>", methods=['PUT'])
def update(prod_id):
    data = request.get_json()
    prod = repo.Product(id=prod_id, name=data['name'], qty=data['qty'], price=data['price'])
    repo.update_product(prod)
    updated = repo.read_product_by_id(prod_id)
    return jsonify(updated.__dict__)


@app.route("/products/<int:prod_id>", methods=['DELETE'])
def delete(prod_id):
    repo.delete_product(prod_id)
    return jsonify({"status": "deleted"})


@app.route("/stock/total", methods=['GET'])
def total_stock():
    total = stock_calc.total_stock()
    return jsonify({"total_stock": total})


@app.route("/products/scrape", methods=['GET'])
def scrape_products():
    products = scraper.scrape_products()
    return jsonify(products)


if __name__ == "__main__":
    app.run(debug=True)