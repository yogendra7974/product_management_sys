import os
import tempfile
import pytest
import server.product_repo as repo

@pytest.fixture
def temp_db():
    db_fd, temp_path = tempfile.mkstemp()
    repo.DB_PATH = temp_path
    repo.product_table_create()
    yield
    os.close(db_fd)
    os.remove(temp_path)

def test_create_read_product(temp_db):
    product = repo.Product(name="TestProduct", qty=5, price=99.99)
    pid = repo.create_product(product)
    saved = repo.read_product_by_id(pid)
    assert saved.name == "TestProduct"
    assert saved.qty == 5
    assert saved.price == 99.99

def test_update_product(temp_db):
    pid = repo.create_product(repo.Product(name="Old", qty=1, price=10))
    repo.update_product(repo.Product(id=pid, name="New", qty=2, price=20))
    updated = repo.read_product_by_id(pid)
    assert updated.name == "New"
    assert updated.qty == 2
    assert updated.price == 20

def test_delete_product(temp_db):
    pid = repo.create_product(repo.Product(name="DeleteMe", qty=1, price=10))
    repo.delete_product(pid)
    deleted = repo.read_product_by_id(pid)
    assert deleted is None