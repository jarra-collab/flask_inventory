import unittest
from app import app, inventory

class TestInventoryAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        inventory.clear()  # Reset inventory

    def test_add_item(self):
        res = self.client.post("/inventory", json={"name": "Test", "barcode": "123"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(inventory), 1)

    def test_get_inventory(self):
        self.client.post("/inventory", json={"name": "Test", "barcode": "123"})
        res = self.client.get("/inventory")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json), 1)

    def test_update_item(self):
        self.client.post("/inventory", json={"name": "Test", "barcode": "123"})
        res = self.client.patch("/inventory/1", json={"name": "Updated"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["name"], "Updated")

    def test_delete_item(self):
        self.client.post("/inventory", json={"name": "Test", "barcode": "123"})
        res = self.client.delete("/inventory/1")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(inventory), 0)

if __name__ == "__main__":
    unittest.main()