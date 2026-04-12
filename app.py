import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)
JSON_FILE = "inventory.json"
EXTERNAL_API = "https://world.openfoodfacts.org/api/v0/product/{}.json"


# --------------------------
# Helper Functions
# --------------------------
def load_inventory():
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_inventory(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_next_id(inventory):
    if inventory:
        return max(item["id"] for item in inventory) + 1
    return 1


# --------------------------
# Routes
# --------------------------

# Home route
@app.route("/")
def home():
    return "Inventory Management API is running!", 200


# Get all inventory items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    inventory = load_inventory()
    return jsonify(inventory)


# Get single item by ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    inventory = load_inventory()
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


# Add new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.json
    inventory = load_inventory()
    data["id"] = get_next_id(inventory)
    inventory.append(data)
    save_inventory(inventory)
    return jsonify(data), 201


# Update item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.json
    inventory = load_inventory()
    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            save_inventory(inventory)
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


# Delete item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    inventory = load_inventory()
    inventory = [item for item in inventory if item["id"] != item_id]
    save_inventory(inventory)
    return jsonify({"message": "Item deleted"})


# Fetch product from OpenFoodFacts
@app.route("/inventory/fetch", methods=["GET"])
def fetch_external_product():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "Barcode required"}), 400

    response = requests.get(EXTERNAL_API.format(barcode))
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch product"}), 500

    data = response.json()
    product = data.get("product")
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Prepare data for local inventory
    inventory_data = {
        "id": get_next_id(load_inventory()),
        "name": product.get("product_name", "Unknown"),
        "barcode": barcode,
        "quantity": 0,
        "price": 0.0,
        "description": product.get("generic_name", ""),
        "category": product.get("categories", ""),
    }

    # Save to inventory
    inventory = load_inventory()
    inventory.append(inventory_data)
    save_inventory(inventory)

    return jsonify(inventory_data), 201


# --------------------------
# Run the app
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)