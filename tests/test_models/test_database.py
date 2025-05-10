import unittest
import sqlite3
from flask import Flask, g
from models import database

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['DB_PATH'] = ':memory:'  # Use in-memory DB for safe testing

        database.init_app(self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        database.close_db()
        self.ctx.pop()

    def test_get_db_returns_connection(self):
        db = database.get_db()
        self.assertIsInstance(db, sqlite3.Connection)
        self.assertEqual(db, g.db)
        print("✅ get_db() returns a valid SQLite connection.")

    def test_close_db_closes_connection(self):
        db = database.get_db()
        self.assertFalse(db is None)
        database.close_db()
        self.assertNotIn('db', g)
        print("✅ close_db() successfully removes 'db' from Flask's `g` object.")

    def test_init_app_registers_teardown(self):
        with self.app.test_client() as client:
            # This will trigger the teardown after request
            @self.app.route('/test')
            def test_route():
                database.get_db()
                return 'OK'

            response = client.get('/test')
            self.assertEqual(response.status_code, 200)
        print("✅ init_app() registers the teardown callback properly.")

if __name__ == '__main__':
    unittest.main()
