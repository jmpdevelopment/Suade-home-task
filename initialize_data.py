from pathlib import Path
import sqlite3
from os import path
import logging

db_path = 'app/orders_data.db'
data_source_path = 'data/'
test_db_path = 'tests/test.db'
test_data_source_path = 'test data/'

tables_schemas = {
    "commissions": "(id INT PRIMARY KEY, date DATETIME, vendor_id INT, rate FLOAT)",
    "order_lines": "(id INT PRIMARY KEY, order_id INT, product_id INT, product_description TEXT, product_price FLOAT, product_vat_rate FLOAT, discount_rate FLOAT, quantity INT, full_price_amount FLOAT, discounted_amount FLOAT, vat_amount FLOAT, total_amount FLOAT)",
    "orders": "(id INT PRIMARY KEY, created_at DATETIME, vendor_id INT, customer_id INT)",
    "product_promotions": "(id INT PRIMARY KEY, date DATETIME, product_id INT, promotion_id INT)",
    "products": "(id INT PRIMARY KEY, description TEXT)",
    "promotions": "(id INT PRIMARY KEY, description TEXT)",
}

def initialize_data(db_path = db_path, source_path = data_source_path):

    if not path.exists(db_path):
        logging.info("Creating database file....")
        Path(db_path).touch()
        logging.info("Database file created successfully")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    logging.info("Creating tables if not present: %s", tables_schemas)
    for table, columns in tables_schemas.items():
        c.execute('''CREATE TABLE IF NOT EXISTS {table} {columns}'''.format(table=table, columns=columns))

    logging.info("Tables created")

    logging.info("Reading data from raw data folder....")
    import pandas as pd
    commissions = pd.read_csv('%scommissions.csv' % source_path)
    commissions['date'] = pd.to_datetime(commissions['date'], format='%d/%m/%Y')
    order_lines = pd.read_csv('%sorder_lines.csv' % source_path)
    orders = pd.read_csv('%sorders.csv' % source_path)
    product_promotions = pd.read_csv('%sproduct_promotions.csv' % source_path)
    product_promotions['date'] = pd.to_datetime(product_promotions['date'], format='%d/%m/%Y')
    products = pd.read_csv('%sproducts.csv' % source_path)
    promotions = pd.read_csv('%spromotions.csv' % source_path)

    logging.info("Updating tables with data")

    commissions.to_sql('commissions', conn, if_exists='append', index = False)
    order_lines.to_sql('order_lines', conn, if_exists='append', index = False)
    orders.to_sql('orders', conn, if_exists='append', index = False)
    product_promotions.to_sql('product_promotions', conn, if_exists='append', index = False)
    products.to_sql('products', conn, if_exists='append', index = False)
    promotions.to_sql('promotions', conn, if_exists='append', index = False)

    logging.info("Done")

if __name__ == '__main__':
    initialize_data()
