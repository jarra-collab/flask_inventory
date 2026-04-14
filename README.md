# 📦 Flask Inventory Management System

A simple Inventory Management System built with **Flask (REST API)**, a **Python CLI client**, and **unit tests using pytest**.  
It also integrates with the **OpenFoodFacts API** to fetch product details using barcodes.

---

## 🚀 Features

### 🔹 REST API (Flask)
- Create inventory items
- Read all items
- Read single item
- Update items (PATCH)
- Delete items
- Persistent storage using `inventory.json`

### 🔹 External API Integration
- Fetch product details using barcode
- Uses OpenFoodFacts API
- Automatically adds fetched products to inventory

### 🔹 CLI Interface
- Add items via terminal
- List all items
- Update items
- Delete items
- Fetch products by barcode

### 🔹 Unit Testing (pytest)
- Tests for all CRUD operations
- API response validation
- Test client using Flask `test_client`
- Clean test isolation

---

## 🏗️ Project Structure
flask_inventory/
│
├── app.py # Flask REST API
├── cli.py # Command-line interface
├── inventory.json # Data storage file
├── test_app.py # pytest unit tests
└── README.md