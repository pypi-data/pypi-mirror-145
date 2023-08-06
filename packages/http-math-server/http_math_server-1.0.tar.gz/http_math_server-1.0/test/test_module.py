import unittest

from ..src import models, config, http_server
from ..src.calculation import calculate


class TestCalculation(unittest.TestCase):

    def setUp(self):
        http_server.app.testing = True
        self.app = http_server.app.test_client()


    def test_main_page(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)


    def test_right_calculation(self):
        self.assertEqual(float(calculate("add 1 2")['result']), 3)
        self.assertEqual(float(calculate("pow 4 2")['result']), 16)
        self.assertEqual(float(calculate("sub 1 2")['result']), -1)
        self.assertEqual(float(calculate("truediv 1 2")['result']), 0.5)
        self.assertEqual(float(calculate("mul 1 2")['result']), 2)


    def test_raising_Error(self):
        strings = {
            "string_index_err": "add 1 2 3",
            "string_value_err": "add one two",
            "string_zero_div_err": "truediv 1 0",
            "string_attr_err": "div 1 2"
        }

        self.assertIn('ValueError', calculate(strings["string_index_err"]))
        self.assertIn('ValueError', calculate(strings["string_value_err"]))
        self.assertIn('ZeroDivisionError', calculate(strings["string_zero_div_err"]))
        self.assertIn('AttributeError', calculate(strings["string_attr_err"]))


class TestDatabase(unittest.TestCase):

    def setUp(self):

        user = config.DB_USER
        password = config.DB_PASS
        host = config.DB_HOST
        port = config.DB_PORT
        db_name = 'testdb'

        self.db = models.UserDatabaseInterfase(
            user,
            password,
            host,
            port,
            db_name
        )

        self.db.create_database()
        self.engine = self.db._UserDatabaseInterfase__engine
        self.session = self.db._UserDatabaseInterfase__session
        self.connection = self.engine.connect()


    def tearDown(self):
        self.db.drop_table()


    def test_append_data(self):
        data = {
            'operator': 'add',
            'num1': 1,
            'num2': 2,
            'result': 3.0
        }

        self.db.insert_data(data)

        row_request = self.session.query(models.DataModel)
        response = self.connection.execute(str(row_request))
        self.assertTrue(len(response.fetchall()))
        self.connection.close()
