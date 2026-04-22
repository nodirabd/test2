import sqlite3

from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.products_table)
    conn.commit()
    conn.close()


def add_product(product_name, quantity):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.insert_product, (product_name, quantity))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


def update_product(product_id, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if completed is not None:
        cursor.execute(queries.update_product_completed, (completed, product_id))

    conn.commit()
    conn.close()


def get_products(filter_type):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'all':
        cursor.execute(queries.select_products)
    elif filter_type == 'completed':
        cursor.execute(queries.select_products_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_products_uncompleted)

    products = cursor.fetchall()
    conn.close()
    return products


def delete_product(product_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_product, (product_id,))
    conn.commit()
    conn.close()


"""def get_completed_count():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.count_completed_products)
    count = cursor.fetchone()[0]
    conn.close()
    return count"""
def get_completed_count():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.get_completed_count)
    result = cursor.fetchone()
    conn.close()
    # result[0] будет None, если купленных товаров нет
    if result is not None and result[0] is not None:
        return result[0]
    
    return 0  # Если товаров нет, возвращаем ноль

