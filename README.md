# FarmStore - Agriculture E-commerce Website

A full working project: PostgreSQL database, Python (Flask) backend, HTML/CSS/JS frontend.

## Folder structure
```
farm-store/
├── database/
│   └── schema.sql       -> run once in PostgreSQL to create tables + sample data
├── backend/
│   ├── app.py            -> run this file: python app.py
│   ├── db.py              -> all database queries
│   ├── auth_utils.py      -> password hashing
│   ├── requirements.txt
│   └── .env.example       -> copy to .env and fill your DB password
└── frontend/
    ├── index.html, products.html, product.html, cart.html,
    │   login.html, register.html, orders.html, admin.html
    ├── css/style.css
    └── js/api.js, cart.js, auth.js
```

## Setup steps
See the chat message for the full step-by-step guide. Quick version:

1. Create database in PostgreSQL: `CREATE DATABASE farmstore;`
2. Run `database/schema.sql` against that database.
3. `cd backend`, create venv, `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, fill in your PostgreSQL password.
5. `python app.py`
6. Open http://localhost:5000

## Test accounts
- Admin login: `[email protected]` / `admin123`
- Or register a new customer account from the Register page.
