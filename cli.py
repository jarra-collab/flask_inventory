import requests
import argparse

API_URL = "http://127.0.0.1:5000/inventory"

# --------------------------
# CLI Functions
# --------------------------

def list_items():
    res = requests.get(API_URL)
    if res.ok:
        print(res.json())
    else:
        print("Failed to fetch items")


def add_item(name, barcode, quantity, price, description, category):
    data = {
        "name": name,
        "barcode": barcode,
        "quantity": quantity,
        "price": price,
        "description": description,
        "category": category,
    }
    res = requests.post(API_URL, json=data)
    if res.ok:
        print("Item added:", res.json())
    else:
        print("Failed to add item")


def fetch_item(barcode):
    res = requests.get(f"{API_URL}/fetch?barcode={barcode}")
    if res.ok:
        print("Fetched item:", res.json())
    else:
        print("Failed to fetch item")


def delete_item(item_id):
    res = requests.delete(f"{API_URL}/{item_id}")
    if res.ok:
        print(res.json())
    else:
        print("Failed to delete item")


def update_item(item_id, name=None, quantity=None, price=None):
    data = {}
    if name:
        data["name"] = name
    if quantity is not None:
        data["quantity"] = quantity
    if price is not None:
        data["price"] = price
    res = requests.patch(f"{API_URL}/{item_id}", json=data)
    if res.ok:
        print("Updated:", res.json())
    else:
        print("Failed to update item")


# --------------------------
# CLI Argument Parser
# --------------------------
parser = argparse.ArgumentParser(description="Inventory CLI")
subparsers = parser.add_subparsers(dest="command")

# list
subparsers.add_parser("list")

# add
add_parser = subparsers.add_parser("add")
add_parser.add_argument("--name", required=True)
add_parser.add_argument("--barcode", required=True)
add_parser.add_argument("--quantity", type=int, default=0)
add_parser.add_argument("--price", type=float, default=0.0)
add_parser.add_argument("--description", default="")
add_parser.add_argument("--category", default="")

# fetch
fetch_parser = subparsers.add_parser("fetch")
fetch_parser.add_argument("--barcode", required=True)

# delete
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("--id", type=int, required=True)

# update
update_parser = subparsers.add_parser("update")
update_parser.add_argument("--id", type=int, required=True)
update_parser.add_argument("--name")
update_parser.add_argument("--quantity", type=int)
update_parser.add_argument("--price", type=float)

args = parser.parse_args()

# --------------------------
# Execute commands
# --------------------------
if args.command == "list":
    list_items()
elif args.command == "add":
    add_item(args.name, args.barcode, args.quantity, args.price, args.description, args.category)
elif args.command == "fetch":
    fetch_item(args.barcode)
elif args.command == "delete":
    delete_item(args.id)
elif args.command == "update":
    update_item(args.id, args.name, args.quantity, args.price)
else:
    parser.print_help()