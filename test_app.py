import json
import pytest
from app import app


# --------------------------
# Fixture
# --------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True

    # reset JSON file before each test
    with open("inventory.json", "w") as f:
        json.dump([], f)

    with app.test_client() as client:
        yield client


# --------------------------
# Tests
# --------------------------

def test_add_item(client):
    res = client.post("/inventory", json={
        "name": "Test",
        "barcode": "123"
    })

    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Test"


def test_get_inventory(client):
    client.post("/inventory", json={"name": "Test", "barcode": "123"})

    res = client.get("/inventory")

    assert res.status_code == 200
    assert len(res.get_json()) == 1


def test_update_item(client):
    client.post("/inventory", json={"name": "Test", "barcode": "123"})

    res = client.patch("/inventory/1", json={"name": "Updated"})

    assert res.status_code == 200
    assert res.get_json()["name"] == "Updated"


def test_delete_item(client):
    client.post("/inventory", json={"name": "Test", "barcode": "123"})

    res = client.delete("/inventory/1")
    assert res.status_code == 200

    res2 = client.get("/inventory")
    assert len(res2.get_json()) == 0


def test_get_not_found(client):
    res = client.get("/inventory/999")
    assert res.status_code == 404