# C - R - U - D

products_table = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        completed INTEGER DEFAULT 0
    )
"""

insert_product = 'INSERT INTO products (product_name, quantity) VALUES (?, ?)'
select_products = 'SELECT * FROM products'
select_products_completed = 'SELECT * FROM products WHERE completed = 1'
select_products_uncompleted = 'SELECT * FROM products WHERE completed = 0'
update_product_completed = 'UPDATE products SET completed = ? WHERE id = ?'
delete_product = 'DELETE FROM products WHERE id = ?'
get_completed_count = 'SELECT SUM(quantity) FROM products WHERE completed = 1'