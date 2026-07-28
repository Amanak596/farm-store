-- =========================================================
-- FarmStore Database Schema
-- Run this file once to create all tables + starter data
-- =========================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

-- ---------------------------------------------------------
-- USERS  (customers + admin)
-- ---------------------------------------------------------
CREATE TABLE users (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(150) UNIQUE NOT NULL,
    password_hash  VARCHAR(200) NOT NULL,
    address        VARCHAR(255),
    phone          VARCHAR(20),
    is_admin       BOOLEAN DEFAULT FALSE,
    created_at     TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- CATEGORIES  (Fertilizers, Tractors, Drones, Tools ...)
-- ---------------------------------------------------------
CREATE TABLE categories (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100) UNIQUE NOT NULL
);

-- ---------------------------------------------------------
-- PRODUCTS
-- ---------------------------------------------------------
CREATE TABLE products (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    description   TEXT,
    price         NUMERIC(10, 2) NOT NULL,
    quantity      INTEGER NOT NULL DEFAULT 0,
    image_url     VARCHAR(500),
    category_id   INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at    TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- ORDERS
-- ---------------------------------------------------------
CREATE TABLE orders (
    id            SERIAL PRIMARY KEY,
    user_id       INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total_amount  NUMERIC(10, 2) NOT NULL,
    status        VARCHAR(30) DEFAULT 'placed',
    address       VARCHAR(255),
    created_at    TIMESTAMP DEFAULT NOW()
);

-- ---------------------------------------------------------
-- ORDER ITEMS  (products inside an order)
-- ---------------------------------------------------------
CREATE TABLE order_items (
    id           SERIAL PRIMARY KEY,
    order_id     INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id   INTEGER REFERENCES products(id),
    quantity     INTEGER NOT NULL,
    price        NUMERIC(10, 2) NOT NULL   -- price at the time of order
);

-- =========================================================
-- SEED DATA
-- =========================================================

-- Admin account -> email: [email protected]  password: admin123
INSERT INTO users (name, email, password_hash, address, phone, is_admin)
VALUES ('Admin', '[email protected]',
        'adminfixedsalt01$4fa812d2133a2ccc194ae587d468c37a11cbcf32cd23da48dfb2ec3d97dbf733',
        'Farm Store HQ', '9999999999', TRUE);

-- Categories
INSERT INTO categories (name) VALUES
('Fertilizers'),
('Tractors'),
('Drones'),
('Tools');

-- Products
INSERT INTO products (name, description, price, quantity, image_url, category_id) VALUES
('Urea Fertilizer 50kg', 'High nitrogen urea fertilizer, ideal for cereal crops.', 850.00, 100, 'https://placehold.co/300x200?text=Urea+Fertilizer', 1),
('DAP Fertilizer 50kg', 'Di-Ammonium Phosphate for root development.', 1400.00, 80, 'https://placehold.co/300x200?text=DAP+Fertilizer', 1),
('Organic Compost 25kg', 'Fully organic compost for all soil types.', 600.00, 120, 'https://placehold.co/300x200?text=Organic+Compost', 1),

('Mini Tractor 20HP', 'Compact tractor suitable for small farms.', 350000.00, 5, 'https://placehold.co/300x200?text=Mini+Tractor', 2),
('Heavy Duty Tractor 55HP', 'Powerful tractor for large-scale farming.', 750000.00, 3, 'https://placehold.co/300x200?text=Heavy+Tractor', 2),

('Agri Spray Drone', 'Drone for pesticide and fertilizer spraying, 10L tank.', 180000.00, 8, 'https://placehold.co/300x200?text=Spray+Drone', 3),
('Crop Monitoring Drone', 'Camera drone for crop health monitoring.', 95000.00, 10, 'https://placehold.co/300x200?text=Monitor+Drone', 3),

('Hand Cultivator', 'Sturdy hand cultivator for soil loosening.', 450.00, 200, 'https://placehold.co/300x200?text=Hand+Cultivator', 4),
('Sprayer Pump 16L', 'Manual backpack sprayer pump.', 1200.00, 60, 'https://placehold.co/300x200?text=Sprayer+Pump', 4),
('Sickle Set', 'Set of 3 sharp sickles for harvesting.', 350.00, 150, 'https://placehold.co/300x200?text=Sickle+Set', 4);
