"""
db.py
------------------------------------------------------------
This file is ONLY responsible for talking to the PostgreSQL
database. app.py never writes raw SQL itself - it calls the
functions in this file. This keeps "database code" and
"backend logic" cleanly separated.
------------------------------------------------------------
"""

import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()  # reads the .env file


def get_connection():
    """Opens a new connection to the PostgreSQL database."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "farmstore"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        row_factory=dict_row,
    )


def query(sql, params=None, fetch="all"):
    """
    Runs a SQL query.
    fetch = "all"  -> returns list of rows (as dicts)
    fetch = "one"  -> returns a single row (as dict) or None
    fetch = "none" -> used for INSERT/UPDATE/DELETE with no return value
    fetch = "id"   -> used for INSERT ... RETURNING id  -> returns that id
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())

        result = None
        if fetch == "all":
            result = cur.fetchall()
        elif fetch == "one":
            result = cur.fetchone()
        elif fetch == "id":
            row = cur.fetchone()
            result = row["id"] if row else None

        conn.commit()
        cur.close()
        return result
    finally:
        conn.close()


# ---------------------------------------------------------
# USERS
# ---------------------------------------------------------
def get_user_by_email(email):
    return query("SELECT * FROM users WHERE email = %s", (email,), fetch="one")


def get_user_by_id(user_id):
    return query("SELECT * FROM users WHERE id = %s", (user_id,), fetch="one")


def create_user(name, email, password_hash, address, phone):
    return query(
        """INSERT INTO users (name, email, password_hash, address, phone)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (name, email, password_hash, address, phone),
        fetch="id",
    )


# ---------------------------------------------------------
# CATEGORIES
# ---------------------------------------------------------
def get_categories():
    return query("SELECT * FROM categories ORDER BY name")


# ---------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------
def get_products(category_id=None):
    if category_id:
        return query(
            "SELECT * FROM products WHERE category_id = %s ORDER BY id",
            (category_id,),
        )
    return query("SELECT * FROM products ORDER BY id")


def get_product_by_id(product_id):
    return query("SELECT * FROM products WHERE id = %s", (product_id,), fetch="one")


def reduce_product_stock(product_id, quantity):
    query(
        "UPDATE products SET quantity = quantity - %s WHERE id = %s",
        (quantity, product_id),
        fetch="none",
    )


def create_product(name, description, price, quantity, image_url, category_id):
    return query(
        """INSERT INTO products (name, description, price, quantity, image_url, category_id)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (name, description, price, quantity, image_url, category_id),
        fetch="id",
    )


# ---------------------------------------------------------
# ORDERS
# ---------------------------------------------------------
def create_order(user_id, total_amount, address):
    return query(
        """INSERT INTO orders (user_id, total_amount, address)
           VALUES (%s, %s, %s) RETURNING id""",
        (user_id, total_amount, address),
        fetch="id",
    )


def add_order_item(order_id, product_id, quantity, price):
    query(
        """INSERT INTO order_items (order_id, product_id, quantity, price)
           VALUES (%s, %s, %s, %s)""",
        (order_id, product_id, quantity, price),
        fetch="none",
    )


def get_orders_for_user(user_id):
    return query(
        "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )


def get_order_items(order_id):
    return query(
        """SELECT oi.*, p.name AS product_name, p.image_url
           FROM order_items oi
           JOIN products p ON p.id = oi.product_id
           WHERE oi.order_id = %s""",
        (order_id,),
    )


def get_order_by_id(order_id):
    return query("SELECT * FROM orders WHERE id = %s", (order_id,), fetch="one")


def get_all_orders():
    """Admin: every order, with the customer's name/email attached."""
    return query(
        """SELECT o.*, u.name AS customer_name, u.email AS customer_email
           FROM orders o
           JOIN users u ON u.id = o.user_id
           ORDER BY o.created_at DESC"""
    )
