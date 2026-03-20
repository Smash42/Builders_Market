
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS user_roles;
DROP TABLE IF EXISTS role_permissions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;

/* Ensure all users are unique with username and email, password will be hashed */
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* Define Role options for users */
CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* Permissions that can be assigned to roles */
CREATE TABLE permissions (
    permission_id INTEGER PRIMARY KEY, 
    permission_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* Connects Roles to th Permissions they have */
CREATE TABLE role_permissions (
    role_id INTEGER,
    permission_id INTEGER,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE
);

/* Connect Users to their Roles  */
CREATE TABLE user_roles (
    user_id INTEGER,
    role_id INTEGER,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
);

/* Table with all the Products available  */
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    image_file TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* Table for storing orders */
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

/* Table to connect Orders and Products with quantity and price purchased at */
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

/* Table to define Product Categories */
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(25) NOT NULL UNIQUE
);

/* Connects Product to their respective categories */
CREATE TABLE product_categories (
    product_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

/* Table for user reviews on products */
CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 0 AND rating <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

/* Setting the 3 Roles that can be given to users */
INSERT INTO roles (role_id, role_name, description) VALUES 
(1, 'Admin', 'Full access to all features and settings'),
(2, 'Moderator', 'Can manage content, products, and users'),
(3, 'User', 'Standard user, can modify their own order and reviews');

/* Adding all the Permissions, with descriptions, that are to be assigned to roles  */
INSERT INTO permissions (permission_id, permission_name, description) VALUES 
(1, 'product.add', 'Created new products in Database'),
(2, 'product.edit', 'Edits existing products information'),
(3, 'product.delete', 'Removes products from database'),
(4, 'order.item.add', 'Add item to users order'),
(5, 'order.item.edit', 'Modify item in users order'),
(6, 'order.item.delete', 'Delete item in a users order'),
(7, 'order.add', 'Created an order'),
(8, 'order.edit', 'Modify order'),
(9, 'order.delete.own', 'Removes orders created by the user'),
(10, 'order.delete.all', 'Removes any order in the database'),
(11, 'review.add', 'Add new review to a product'),
(12, 'review.edit.own', 'Modify own review'),
(13, 'review.edit.all', 'Modify any review'),
(14, 'review.delete.own', 'Remove review created by the user'),
(15, 'review.delete.all', 'Removes any review in the database'),
(16, 'role.add', 'Create new roles'),
(17, 'role.edit', 'Modify existing roles'),
(18, 'role.read', 'Review role details'),
(19, 'role.delete', 'Remove roles from database'),
(20, 'user.changerole', 'Change a users assigned role'),
(21, 'category.add', 'Create new product categories'),
(22, 'user.delete', 'Remove a user and their information'),
(23, 'user.edit', 'Modify a user'),
(24, 'category.delete', 'Remove product categories');

/* Assign Permission to Roles */
INSERT INTO role_permissions (role_id, permission_id) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12),
(1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23),(1,24),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2,9), (2,10), (2,11), (2,12), (2,13), (2,14), (2,15), (2,21), (2,24),
(3, 4), (3,5), (3,6), (3, 7), (3,9), (3, 11), (3, 12), (3, 14);

/* Inserting some initial Products into the database */
INSERT INTO products (product_id, product_name, description, price, quantity, image_file) VALUES 
(1, 'DeWalt Miter Saw', '12 inch blade, 15 amp motor.', 349.99, 15, 'dewalt_miter.jpg'),
(2, 'Milwaukee Brushless Impact Drill', '18V lithium-ion battery, 1/4 inch drive.', 129.99, 50, 'milwaukee_impact.jpg'),
(3, 'Wine Glass Bottle Holder', 'Fit two wine glasses on either side of the wine bottle with this holder', 49.99, 20, 'wine_glass_holder.jpg'),
(4, 'Bottle Cap Plinko', 'User your bottle cap to play Plinko and see what you land in', 75.99, 12, 'drinko_plinko.jpg'),
(5, 'Shot Wheel', 'Spin the wheel and see what you land on', 59.99, 10, 'shot_wheel.jpg');

/* Inserting some initial Categories into the database */
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Tools'),
(2, 'Drinks Accessories'),
(3, 'Games');

/* Assigning initial Products to their Categories */
INSERT INTO product_categories (product_id, category_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3),
(5, 3);

/* Setting up a user account, password would need to be encrypted */
INSERT INTO users (user_id, username, email, password_hash) VALUES
(1, 'Jack Hughes', 'njdevils@test.com', 'scrypt:32768:8:1$p4fHWQaIXEH2HTMt$4e4cf6fd878639c8b982d870072d2d53312d40e21f2c3646521d7e885380f77cdd4008402518af754dc829f22f2e0af7f0119caa55e59b1e999d41f6dd3d1417!'),
(2, 'Aaron Rodgers', 'gopackr@test.com', 'hashed_password_456'),
(3, 'Kelly Slater', 'surfsup@test.com', 'hashed_password_789');

/* Assign role to initial users */
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1),
(2, 2),
(3, 3);

/* Inputting a test Order for the test user */
INSERT INTO orders (order_id, user_id, status, total) VALUES
(1, 3, 'Pending', 129.99);

/* Input order items for the test order1 */
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, purchase_price) VALUES
(1, 1, 2, 1, 129.99),
(2, 1, 5, 1, 59.99);

/* Inputting a test review for a product by the test user */
INSERT INTO reviews (review_id, product_id, user_id, rating) VALUES
(1, 2, 3, 5);