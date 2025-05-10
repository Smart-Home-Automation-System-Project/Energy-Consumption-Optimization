import unittest
import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask
from models.database import init_app, get_db
from models.historical_data import HistoricalData

class TestHistoricalDataModel(unittest.TestCase):
    def setUp(self):
        # Setup temp DB
        self.app = Flask(__name__)
        self.db_fd, self.db_path = os.pipe()
        self.app.config['DB_PATH'] = ':memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_app(self.app)

        self._create_tables()
        self._insert_test_data()

    def tearDown(self):
        self.app_context.pop()

    def _create_tables(self):
        db = get_db()
        db.execute("""
            CREATE TABLE devices (
                switch_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT,
                device_type TEXT,
                max_power_rating REAL,
                status TEXT
            )
        """)
        db.execute("""
            CREATE TABLE historical_energy_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                switch_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                power_consumption REAL NOT NULL,
                FOREIGN KEY (switch_id) REFERENCES devices (switch_id)
            )
        """)
        db.commit()

    def _insert_test_data(self):
        db = get_db()
        db.execute("INSERT INTO devices VALUES (1, 'Device A', 'Room 1', 'Light', 60, 'on')")
        db.execute("INSERT INTO devices VALUES (2, 'Device B', 'Room 2', 'Fan', 75, 'off')")

        now = datetime.now()
        data = [
            (1, (now - timedelta(days=1)).strftime('%Y-%m-%d'), 100),
            (1, (now - timedelta(days=2)).strftime('%Y-%m-%d'), 150),
            (2, (now - timedelta(days=1)).strftime('%Y-%m-%d'), 80),
        ]
        for switch_id, timestamp, power in data:
            db.execute("INSERT INTO historical_energy_readings (switch_id, timestamp, power_consumption) VALUES (?, ?, ?)", (switch_id, timestamp, power))
        db.commit()

    def test_total_consumption_default_range(self):
        results = HistoricalData.get_total_consumption()
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn('date', results[0])
        self.assertIn('total_consumption', results[0])
        print("✅ total_consumption() with default range returns valid data.")

    def test_total_consumption_specific_range(self):
        start = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        end = datetime.now().strftime('%Y-%m-%d')
        results = HistoricalData.get_total_consumption(start, end)
        self.assertGreaterEqual(len(results), 1)
        print("✅ total_consumption() with specific date range returns valid data.")

    def test_total_consumption_empty_result(self):
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        results = HistoricalData.get_total_consumption(future_date, future_date)
        self.assertEqual(results, [])
        print("✅ total_consumption() returns empty list when no data exists.")

    def test_consumption_by_device_default_range(self):
        results = HistoricalData.get_consumption_by_device()
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn('device_name', results[0])
        self.assertIn('energy_consumption', results[0])
        print("✅ consumption_by_device() returns valid device data.")

    def test_consumption_by_device_empty_result(self):
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
        results = HistoricalData.get_consumption_by_device(future_date, future_date)
        self.assertEqual(results, [])
        print("✅ consumption_by_device() returns empty list when no device data exists.")

if __name__ == '__main__':
    unittest.main()
