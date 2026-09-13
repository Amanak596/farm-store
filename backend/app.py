"""
app.py
------------------------------------------------------------
Main backend file. This is the ONLY file you run:
        python app.py

It does two things:
 1. Serves the frontend (the HTML/CSS/JS files in ../frontend)
 2. Provides the API the frontend calls (everything under /api/...)

All database work is delegated to db.py
All password hashing is delegated to auth_utils.py
------------------------------------------------------------
"""

import os
from functools import wraps
from flask import Flask, request, jsonify, session, send_from_directory
from dotenv import load_dotenv

import db
from auth_utils import hash_password, verify_password

load_dotenv()

FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_FOLDER, static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


# =============================================================
# HELPERS
# =============================================================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Please log in first"}), 401
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Please log in first"}), 401
        if not session.get("is_admin"):
            return jsonify({"error": "Admins only"}), 403
        return f(*args, **kwargs)
    return wrapper


# =============================================================
# SERVE FRONTEND PAGES
# =============================================================
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


# (Flask's static_folder setting above already serves every other
#  frontend file automatically, e.g. /products.html, /css/style.css)


# =============================================================
# AUTH  -  register / login / logout / me
# =============================================================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    address = (data.get("address") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not name or not email or not password or not address:
        return jsonify({"error": "Name, email, password and address are required"}), 400

    if db.get_user_by_email(email):
        return jsonify({"error": "An account with this email already exists"}), 400

    password_hash = hash_password(password)
    user_id = db.create_user(name, email, password_hash, address, phone)

    session["user_id"] = user_id
    session["is_admin"] = False
    return jsonify({"message": "Account created", "user_id": user_id})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = db.get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        return jsonify({"error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]
    session["is_admin"] = user["is_admin"]
    return jsonify({
        "message": "Logged in",
        "name": user["name"],
        "is_admin": user["is_admin"],
    })


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/api/me")
def me():
    if "user_id" not in session:
        return jsonify({"logged_in": False})
    user = db.get_user_by_id(session["user_id"])
    return jsonify({
        "logged_in": True,
        "name": user["name"],
        "email": user["email"],
        "address": user["address"],
        "is_admin": user["is_admin"],
    })


# =============================================================
# CATEGORIES & PRODUCTS  (public - no login needed)
# =============================================================
@app.route("/api/categories")
def categories():
    return jsonify(db.get_categories())


@app.route("/api/products")
def products():
    category_id = request.args.get("category_id")
    return jsonify(db.get_products(category_id))


@app.route("/api/products/<int:product_id>")
def product_detail(product_id):
    product = db.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


# =============================================================
# ORDERS  (customer must be logged in)
# =============================================================
@app.route("/api/orders", methods=["POST"])
@login_required
def place_order():
    data = request.get_json()
    items = data.get("items", [])  # [{product_id, quantity}, ...]
    address = data.get("address") or ""

    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    total = 0
    validated_items = []

    for item in items:
        product = db.get_product_by_id(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 400
        qty = int(item["quantity"])
        if qty <= 0 or qty > product["quantity"]:
            return jsonify({"error": f"Not enough stock for {product['name']}"}), 400
        total += float(product["price"]) * qty
        validated_items.append((product, qty))

    order_id = db.create_order(session["user_id"], total, address)

    for product, qty in validated_items:
        db.add_order_item(order_id, product["id"], qty, product["price"])
        db.reduce_product_stock(product["id"], qty)

    return jsonify({"message": "Order placed", "order_id": order_id, "total": total})


@app.route("/api/orders")
@login_required
def my_orders():
    orders = db.get_orders_for_user(session["user_id"])
    for order in orders:
        order["items"] = db.get_order_items(order["id"])
    return jsonify(orders)


@app.route("/api/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    order = db.get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    if order["user_id"] != session["user_id"] and not session.get("is_admin"):
        return jsonify({"error": "Not allowed"}), 403
    order["items"] = db.get_order_items(order_id)
    return jsonify(order)


# =============================================================
# ADMIN  (admin login required)
# =============================================================
@app.route("/api/admin/orders")
@admin_required
def admin_all_orders():
    orders = db.get_all_orders()
    for order in orders:
        order["items"] = db.get_order_items(order["id"])
    return jsonify(orders)


@app.route("/api/admin/products", methods=["POST"])
@admin_required
def admin_add_product():
    data = request.get_json()
    product_id = db.create_product(
        name=data.get("name"),
        description=data.get("description", ""),
        price=data.get("price"),
        quantity=data.get("quantity"),
        image_url=data.get("image_url", ""),
        category_id=data.get("category_id"),
    )
    return jsonify({"message": "Product added", "product_id": product_id})


# =============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
