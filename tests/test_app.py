import os
import unittest
from app import create_app
import json
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):

    def setUp(self):
        app = create_app()       
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/test.db'
        self.app = app.test_client()

    def test_order_data_by_date(self):
        response = self.app.get('/api/v1/orders_data_by_date?date=20190801')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get("customers"), 9)
        self.assertEqual(data.get("commissions"), {'order_average': 2314804.1, 'promotions': {'1': 0, '2': 188049.4, '3': 0, '4': 0, '5': 1153804.8}, 'total': 20833236.94})
        self.assertEqual(data.get("discount_rate_avg"), 0.13)
        self.assertEqual(data.get("items"), 2895)
        self.assertEqual(data.get("order_total_avg"), 1182286.1)
        self.assertEqual(data.get("total_discount_amount"), 130429980.26)

    def test_order_data_by_date_no_data_on_date(self):
        response = self.app.get('/api/v1/orders_data_by_date?date=20190802')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data.get("customers"), 0)
        self.assertEqual(data.get("commissions"), {'order_average': 0, 'promotions': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}, 'total': 0})
        self.assertEqual(data.get("discount_rate_avg"), 0)
        self.assertEqual(data.get("items"), 0)
        self.assertEqual(data.get("order_total_avg"), 0)
        self.assertEqual(data.get("total_discount_amount"), 0)

    def test_order_data_by_date_bad_input(self):
        response = self.app.get('/api/v1/orders_data_by_date?date=2019/08/01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Error: Please specify a date in yyyymmdd format e.g. 20210329, your input was: 2019/08/01")

    def test_order_data_by_date_no_input(self):
        response = self.app.get('/api/v1/orders_data_by_date')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Error: No date field provided. Please specify a date in yyyymmdd format e.g. 202103289")
 
 
if __name__ == "__main__":
    unittest.main()